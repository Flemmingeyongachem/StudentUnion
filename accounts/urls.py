from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from django.contrib.auth import views as auth

app_name="accounts"

urlpatterns = [
     path('', auth.LogoutView.as_view(next_page ='login'), name ='logout'),
     path('login/', Login, name ='login'),
     path('profile/', profile, name ='profile'),
     path('signup/', register, name ='signup'),
]