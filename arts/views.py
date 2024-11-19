from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from .models import Art
from .forms import UpdateArt, AddArt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
class ArtistView(ListView):
    model = Art
    template_name = 'index.html'
    context_object_name = 'arts'
    paginate_by = 8  

    def get_queryset(self):
        user_id = self.request.user.id
        return Art.objects.filter(owner=user_id).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for art in context['arts']:
            art.is_image = art.is_image()
            art.is_video = art.is_video()
        return context
class GalleryView(ListView):
    model=Art
    template_name='gallery.html'
    context_object_name = 'arts'
    def get_queryset(self):
        return Art.objects.filter(is_public=True)

class DetailsArtView(DetailView):
    model = Art
    template_name = "art_details.html"  # Template de détails pour afficher une œuvre
    context_object_name = 'art'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art = context.get('art')

        if art:
            art.is_image = art.is_image()  # Use model method
            art.is_video = art.is_video()  # Use model method

        # PayPal configuration
        host = self.request.get_host()
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': art.price,
            'item_name': art.title,
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('payment-success', kwargs={'art_id': art.id})}",
            'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'art_id': art.id})}",
        }

        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        context['paypal'] = paypal_payment

        return context


class DeleteArtView(DeleteView):
    model = Art
    template_name = "art_delete.html"  # Template de confirmation de suppression
    context_object_name = 'art'
    def get_success_url(self):
        return reverse_lazy("list_arts")  # Redirection après suppression

class UpdateArtView(UpdateView):
    model = Art
    template_name = "art_update.html"  # Template de mise à jour de l'œuvre
    form_class = UpdateArt
    context_object_name = 'art'

    def get_success_url(self):
        return reverse_lazy("list_arts")  # Rediriger vers la liste des œuvres après la mise à jour

class CreateArtView(CreateView):
    model = Art
    template_name = "art_create.html"  # Template de création de l'œuvre
    form_class = AddArt
    context_object_name = 'art'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list_arts")  # Rediriger vers la liste des œuvres après la création
class UpdateIsPublicView(View):
    def post(self, request, art_id):
        # Récupérer l'art par son ID
        art = get_object_or_404(Art, id=art_id)
        
        # Inverser la valeur de is_public
        art.is_public = not art.is_public
        art.save()

        # Redirection vers la galerie ou autre page après la mise à jour
        return redirect('gallery')
class ToggleIsPublic(View):
    def get(self, request, art_id):
        # Récupérer l'objet art
        art = get_object_or_404(Art, id=art_id)
        
        # Basculer l'état de is_public
        art.is_public = not art.is_public
        art.save()

        return redirect('list_arts')