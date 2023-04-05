from django import forms
from StudentUnion.models import Student,Level,Department




class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ))




# class UserRegisterForm(UserCreationForm):
class UserRegisterForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "first name",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "last name",
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    matricule_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Matricule",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "confirm password",
                "class": "form-control"
            }
        ))
    picture = forms.ImageField()
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "address",
                "class": "form-control"
            }
        ))
    gender_list = (
        ('female','Female'),
        ('male','Male'),
        )
    levels = Level.objects.all()
    level_list = [(obj.level_name,obj.level_name) for obj in levels]
    
    departments = Department.objects.all()
    department_list = [(obj.dept_name,obj.dept_name) for obj in departments]
    gender = forms.ChoiceField(choices=gender_list)
    my_department = forms.ChoiceField(choices=department_list)
    my_level = forms.ChoiceField(choices=level_list)
    


class UserUpdateForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))
    picture = forms.CharField(
        widget=forms.FileInput(
            attrs={
                "placeholder": "profile picture",
                "class": "form-control"
            }
        ))
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "address",
                "class": "form-control"
            }
        ))

    class Meta:
        model = Student
        fields = ('phone_no','email', 'password1', 'password2',
                  'address','picture')
