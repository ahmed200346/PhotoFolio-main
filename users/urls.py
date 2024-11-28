from django.urls import path
from .views import Register, UserDetails, UpdateView, CustomLogoutView, DetailView, Login, HomeView, UserUpdateView, \
    DeleteUser, AboutView
from django.contrib.auth import views as auth_views
from django.core.mail import send_mail
from django.http import HttpResponse
from . import views
from .views import CustomPasswordResetView
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('details/<int:pk>/', UserDetails.as_view(), name='user_details'),
    path('signup/', Register.as_view(), name='signup'),
    path('', Login.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('logout/', CustomLogoutView.as_view(), name='logout'), 
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', DeleteUser.as_view(), name='delete_user'), 
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),
    path('reset_password_done/', PasswordResetView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),  
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password/password_reset_complete.html'
         ),
         name='password_reset_complete'),   
]