from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import os, datetime
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.urls import reverse
from django.contrib import messages

User = get_user_model()


def user_directory_path(instance, filename):
    profile_pic_name = 'user_{0}/profile.jpg'.format(instance.matricule_number)
    full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)
    return profile_pic_name

def year_choices():
    return [(r,r) for r in range(2001,datetime.date.today().year + 1)]

def current_year():
    return datetime.date.today().year

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.IntegerField(null=True,choices = year_choices(),default=current_year)
    session_end_year = models.IntegerField(null=True,choices = year_choices(),default=current_year)
    session_president = models.OneToOneField(to='Student',on_delete=models.DO_NOTHING,null=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        super(SessionYearModel,self).save(*args, **kwargs)

    def __str__(self):
        return f'{str(self.session_start_year) + " / " + str(self.session_end_year)}'

    class Meta:
        verbose_name_plural = "Academic Year"
 

class Department(models.Model):
    dept_name = models.CharField(max_length=255,primary_key=True)
    
    def __str__(self):
        return f"{self.dept_name}"

class Level(models.Model):
    level_name = models.PositiveSmallIntegerField(primary_key=True)

    def __str__(self):
        return f"{self.level_name}"

class Student(models.Model):
    gender_list = (
        ('female','Female'),
        ('male','Male'),
        )

    my_level = models.ForeignKey(to=Level,on_delete=models.CASCADE,null=True)
    my_department = models.ForeignKey(to=Department,on_delete=models.CASCADE,null=True)
    user = models.OneToOneField(to=User, on_delete = models.CASCADE,null=True,related_name="student_user")
    gender = models.CharField(max_length=30,choices=gender_list,default=gender_list[0])
    address = models.TextField(null=True)
    years_active = models.ManyToManyField(to=SessionYearModel,blank=True)
    matricule_number = models.CharField(max_length=10,primary_key=True)
    picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    USERNAME_FIELD = 'username'
    objects = models.Manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 250, 250
        self.matricule_number = str(self.matricule_number).upper()
        if self.picture:
            pic = Image.open(self.picture.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.picture.path)

    def __str__(self):
        return f'{self.matricule_number}'

    class Meta:
        verbose_name_plural = "Students"



def receipt_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.receipt_owner, filename)

class DueReceipt(models.Model):
    levels = Level.objects.all()
    level_list = [(obj.level_name,obj.level_name) for obj in levels]
    
    departments = Department.objects.all()
    department_list = [(obj.dept_name,obj.dept_name) for obj in departments]

    receipt_owner = models.ForeignKey(to=Student,on_delete=models.CASCADE,null=True,related_name='my_receipts')
    level = models.IntegerField(choices=level_list,null=True)
    department = models.CharField(choices=department_list,null=True,max_length=255)
    file_name = models.ImageField(upload_to=receipt_directory_path,null=True)
    account_name = models.CharField(max_length=255,null=True)
    account_address = models.CharField(max_length=500,null=True)
    our_reference = models.CharField(max_length=16,null=True)
    transaction_amount = models.PositiveIntegerField(null=True,default=0,validators=[MinValueValidator(3000), MaxValueValidator(3000)])
    transaction_account = models.BigIntegerField(null=True)
    is_validated = models.BooleanField(default=False,null=True)
    academic_session = models.ForeignKey(to=SessionYearModel,on_delete=models.CASCADE,null=True)#for eg '2021-2022'


    def get_absolute_url(self):
        return reverse("StudentUnion:create-receipt")

    def __str__(self):
        return f'{self.receipt_owner} {self.academic_session}'
    class Meta:
        verbose_name_plural = "Due Receipts"




@receiver(post_save, sender=DueReceipt)
def update_user_years_active(sender, instance, created, **kwargs):
  if created:
      stud = Student.objects.get(matricule_number=instance.receipt_owner)
      stud.my_level = Level.objects.get(level_name=int(instance.level))
      stud.years_active.add(instance.academic_session)
      stud.save()
    
post_save.connect(update_user_years_active,sender=DueReceipt)




