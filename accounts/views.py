from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

from StudentUnion.models import Student,Level,Department
from .forms import UserRegisterForm,LoginForm,UserUpdateForm
from django.core.mail import send_mail
from django.template.loader import get_template
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse_lazy, reverse



class UserSignUp(FormView):
	redirect_authenticated_user = True
	template_name = "accounts/signup.html"
	form_class = UserRegisterForm
	success_url = reverse_lazy("accounts:login")
	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(UserSignUp, self).form_valid(form)
	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return reverse('StudentUnion:home')
		return super(UserSignUp, self).get(*args, **kwargs)


class UserLogin(LoginView):
	redirect_authenticated_user = True
	form_class = LoginForm
	template_name = 'accounts/login.html'
	
	def get_success_url(self):
		return reverse_lazy("StudentUnion:home")
	


def register(request):
	if request.method == 'POST':
		# form = UserRegisterForm(request.POST)
		form = UserRegisterForm(request.POST,request.FILES)
		if form.is_valid():
			with transaction.atomic():
				username = form.cleaned_data.get('username')
				email = form.cleaned_data.get('email')
				password1 = form.cleaned_data.get('password1')
				first_name = form.cleaned_data.get('first_name')
				last_name = form.cleaned_data.get('last_name')
				gender = form.cleaned_data.get('gender')
				matricule_number = form.cleaned_data.get('matricule_number')
				address = form.cleaned_data.get('address')
				picture = form.cleaned_data.get('picture')
				my_level = form.cleaned_data.get('my_level')
				my_department = form.cleaned_data.get('my_department')
				level = Level.objects.get(level_name=int(my_level))
				department = Department.objects.get(dept_name=my_department)
				user = User.objects.create(username=username,email=email,first_name=first_name,last_name=last_name)
				user.set_password(password1)
				user.save()
				Student.objects.create(matricule_number=matricule_number,picture=picture,
			    address=address,user=user,gender=gender,
			    my_department=department,my_level=level
				)
				user = authenticate(request, username = username, password = password1)
				if user is not None:
					form = login(request, user)
				return redirect(reverse('StudentUnion:home'))
	else:
		form = UserRegisterForm()
	return render(request, 'accounts/signup.html', {'form': form})

def profile(request):
	return redirect(reverse("StudentUnion:home"))

def Login(request):
	print("i was called here")
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!')
			return redirect(reverse('StudentUnion:home'))
		else:
			messages.info(request, f'account done not exit plz sign in')
	form = LoginForm()
	return render(request, 'accounts/login.html', {'form':form})
