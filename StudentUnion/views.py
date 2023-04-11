from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import DetailView,DeleteView,ListView,CreateView,UpdateView
from .forms import DueReceiptCreateForm,DueReceiptUpdateForm
from .models import DueReceipt,SessionYearModel,Student,Level,Department
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse,JsonResponse 
from reportlab.pdfgen import canvas
from .models import DueReceipt
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class StudentCreateReceiptView(LoginRequiredMixin,CreateView):
    model = DueReceipt
    form_class = DueReceiptCreateForm
    template_name = 'StudentUnion/student_create_receipts.html'

    def form_valid(self, form):
        with transaction.atomic():
            owner = Student.objects.get(user=self.request.user)
            form.instance.receipt_owner = owner
            academic_session = SessionYearModel.objects.last()
            form.instance.academic_session = academic_session
            form.save()
            return super(StudentCreateReceiptView, self).form_valid(form)
    
    
    def get_success_url(self):
        return reverse("StudentUnion:home")

class StudentReceiptsView(LoginRequiredMixin, ListView):
    model = DueReceipt
    template_name = 'StudentUnion/student_all_receipts.html'
    context_object_name = "duereceipts"

    def get_queryset(self):
        # self.request.user.student_user.my_receipts.all()
        stud = Student.objects.get(user=self.request.user)
        year = SessionYearModel.objects.last()
        years = stud.years_active.all()
        qs = self.model.objects.filter(receipt_owner=stud, academic_session=year)
        return qs, years
    def get_context_data(self, *args, **kwargs):
        context = super(StudentReceiptsView, self).get_context_data(*args, **kwargs)
        context['session'] = SessionYearModel.objects.last()
        context['profile'] = self.request.user.student_user
        qs, years = self.get_queryset()
        context['all_sessions'] = years.order_by("-session_start_year")
        context['duereceipts'] = qs
        return context

def get_president(request,pk):
    president = Student.objects.get(matricule_number=pk)
    print(president)
    return HttpResponse(president)

def generate_pdf(request, pk):
    instance = DueReceipt.objects.get(pk=pk)
    
    # Create a new PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{instance.receipt_owner.matricule_number}_{instance.academic_session}.pdf"'
    p = canvas.Canvas(response,pagesize=letter)
    # Open the image file and read its contents
    image_data = default_storage.open(instance.file_name.name, 'rb').read()
    img = ImageReader(ContentFile(image_data))
    p.drawImage(img, 60, 100, width=500, height=600)
    p.setFont('Helvetica', 12)
    p.drawCentredString(letter[0]/3, letter[1]-90, f"Matricule: {instance.receipt_owner.matricule_number}")
    p.drawCentredString(letter[0]/3, letter[1]-70, f"Department: {instance.department}")
    p.drawCentredString(letter[0]/3, letter[1]-50, f"session: {instance.academic_session}")
    p.drawCentredString(letter[0]/3, letter[1]-30, f"Receipt for Level: {instance.level }")
    p.showPage()
    p.save()
    return response

class StudentReceiptsPerYearView(LoginRequiredMixin, ListView):
    model = DueReceipt
    template_name = 'StudentUnion/student_all_receipts.html'
    context_object_name = "duereceipts"

    def get_queryset(self):
        stud = Student.objects.get(user=self.request.user)
        year = SessionYearModel.objects.get(id=self.kwargs['pk'])
        years = stud.years_active.all()
        qs = self.model.objects.filter(receipt_owner=stud, academic_session=year)
        return qs, years
    def get_context_data(self, *args, **kwargs):
        context = super(StudentReceiptsPerYearView, self).get_context_data(*args, **kwargs)
        context['session'] = SessionYearModel.objects.last()
        qs, years = self.get_queryset()
        context['all_sessions'] = years.order_by("-session_start_year")
        context['duereceipts'] = qs
        return context


class StudentReceiptDetailView(LoginRequiredMixin, DetailView):
    model = DueReceipt
    context_object_name = "duereceipt"
    template_name = 'StudentUnion/student_receipt_details.html'

class StudentReceiptUpdateView(LoginRequiredMixin, UpdateView):
    model = DueReceipt
    form_class = DueReceiptUpdateForm
    template_name = 'StudentUnion/student_update_receipt.html'
    def get_success_url(self):
        return redirect(reverse("StudentUnion:home"))

class StudentReceiptDeleteView(LoginRequiredMixin, DeleteView):
    model = DueReceipt
    template_name = 'StudentUnion/student_delete_receipts.html'
    def get_success_url(self):
        return reverse("StudentUnion:home")
    

