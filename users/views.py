from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,UpdateView,DeleteView
from django.urls import reverse
from .forms import RegisterForm,CustomUserChangeForm
from .models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import redirect
from users.urls import*


class Register(CreateView): 
    model=User
    form_class= RegisterForm
    template_name = "signup.html"
    success_url = reverse_lazy('login')

class Login(LoginView):
    template_name="login.html"
    
    def get_success_url(self):        
        return reverse('home')
    

class UserDetails(LoginRequiredMixin, DetailView):
    model = User

    template_name = "details.html"

    context_object_name = "user_details"

class HomeView(LoginRequiredMixin,TemplateView):

    template_name = "home.html"
class AboutView(LoginRequiredMixin,TemplateView):

    template_name = "about.html"

class CustomLogoutView(LogoutView):

    next_page = reverse_lazy('login') 

class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'update.html'
    success_url = reverse_lazy('user_details')  

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Vos informations ont été mises à jour avec succès !')
        return super().form_valid(form)  
    def get_success_url(self):
        return reverse('user_details', kwargs={'pk': self.object.pk})
    
class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'delete.html'  
    context_object_name = 'user'  
    success_url = reverse_lazy('login')
    def get_object(self, queryset=None):
        return self.request.user  
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete() 
        return redirect(self.success_url)