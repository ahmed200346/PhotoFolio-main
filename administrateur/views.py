from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Count
from .models import Admin  
from users.models import User 
from arts.models import Art,Like
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            admin = Admin.objects.get(user=self.request.user)
        except Admin.DoesNotExist:
            messages.error(self.request, "Vous n'êtes pas autorisé à accéder à cette page.")
            return redirect(reverse('login'))
        if admin.post == 'Art':
            context['arts'] = Art.objects.all()
            context['likes'] = Like.objects.all()  # Inclure les likes si le rôle est Art
        elif admin.post == 'Users':
            context['users'] = User.objects.all()
        elif admin.post == 'Paiement':
            context['paiements'] = []  
        elif admin.post == 'Admin':
            context['admins'] = Admin.objects.all()

        # Gestion globale si VIP_Status est True
        if admin.VIP_Status:
            context['arts'] = Art.objects.all()
            context['likes'] = Like.objects.all()  
            context['likes'] = Like.objects.all()
            context['users'] = User.objects.all()
            context['admins'] = Admin.objects.all()
            context['paiements'] = []  

        context['admin'] = admin
        return context
