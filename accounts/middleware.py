from django.shortcuts import redirect
from django.urls import reverse
from StudentUnion.models import DueReceipt, SessionYearModel,Student

class RedirectAuthenticatedUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            year= SessionYearModel.objects.last()
            owner = Student.objects.get(user=request.user.id)
            check = DueReceipt.objects.filter(receipt_owner=owner,academic_session=year).exists()
        except Student.DoesNotExist:
            check = False
        if request.path == reverse('accounts:signup') and request.user.is_authenticated:
            return redirect(reverse('StudentUnion:home'))
        elif request.path == reverse('accounts:login') and request.user.is_authenticated:
            return redirect(reverse('StudentUnion:home'))
        elif request.path == reverse('StudentUnion:create-receipt') and check:
            return redirect(reverse('StudentUnion:home'))
        response = self.get_response(request)
        return response