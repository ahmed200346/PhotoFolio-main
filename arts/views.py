from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from .models import *
from .forms import UpdateArt, AddArt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
import csv
class ExportCommentsCSVView(View):
    def get(self, request, art_id):
        try:
            # Récupérer l'œuvre d'art correspondante
            art = get_object_or_404(Art, id=art_id)

            # Récupérer les commentaires associés à cette œuvre d'art
            comments = art.comments.all()

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{art.title}_comments.csv"'
            writer = csv.writer(response)
            writer.writerow(['Art Title', 'comment', 'Username', 'Created At'])
            for comment in comments:
                writer.writerow([art.title, comment.text, comment.user.username, comment.created_at])

            return response

        except Exception as e:
            # Log the error for debugging
            print(f"Error: {e}")
            return HttpResponse("An error occurred while generating the CSV.", status=500)
class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art_id = self.kwargs.get('art_id')
        context['art'] = get_object_or_404(Art, id=art_id)
        return context
    def form_valid(self, form):
        art_id = self.kwargs.get('art_id')
        art = get_object_or_404(Art, id=art_id)
        form.instance.user = self.request.user
        form.instance.art = art
        return super().form_valid(form)
    def get_success_url(self):
        art_id = self.kwargs.get('art_id')
        return reverse_lazy('add_comment', kwargs={'art_id': art_id})

class DeleteComment(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'

    # Ici, `success_url` sera calculé dynamiquement après la suppression
    def get_success_url(self):
        art_id = self.kwargs.get('art_id')  # Récupération de l'ID de l'article
        return reverse_lazy('add_comment', kwargs={'art_id': art_id})  # Redirection vers la vue addcomment avec l'ID de l'article

    def get_object(self, queryset=None):
        comment_id = self.kwargs.get('comment_id')
        return Comment.objects.get(pk=comment_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art_id = self.kwargs.get('art_id')
        context['art'] = get_object_or_404(Art, id=art_id)
        return context
class CommentView(ListView):
    model = Comment
    template_name = "list_comments.html"
    context_object_name = "comments"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        art_id = self.kwargs.get('art_id')
        context['art'] = get_object_or_404(Art, id=art_id)
        return context

    def get_queryset(self):
        art_id = self.kwargs.get('art_id')
        art = get_object_or_404(Art, id=art_id)
        return art.comments.all()
    

class ArtistView(ListView):
    model = Art
    template_name = 'index.html'
    context_object_name = 'arts'
    paginate_by = 8

    def get_queryset(self):
        user_id = self.request.user.id
        search_query = self.request.GET.get('search', '')
        is_public = self.request.GET.get('is_public', None)
        sort_likes = self.request.GET.get('sort_likes', False)

        queryset = Art.objects.filter(owner=user_id)

        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        if is_public is not None:
            if is_public.lower() == 'true': 
                queryset = queryset.filter(is_public=True)
            elif is_public.lower() == 'false':  
                queryset = queryset.filter(is_public=False)
        queryset = queryset.annotate(like_count=Count('arts_likes'))
        if sort_likes and sort_likes.lower() == 'true':
            queryset = queryset.order_by('-like_count', '-created_at')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset
class GalleryView(ListView):
    model = Art
    template_name = 'gallery.html'
    context_object_name = 'arts'
    paginate_by = 8  # Display 8 items per page

    def get_queryset(self):
        category_filter = self.request.GET.get('category', '')
        favorites_filter = self.request.GET.get('favorites', '')
        queryset = Art.objects.filter(is_public=True)

        if category_filter:
            queryset = queryset.filter(category=category_filter)

        if favorites_filter and self.request.user.is_authenticated:
            liked_art_ids = Like.objects.filter(user=self.request.user).values_list('art_id', flat=True)
            queryset = queryset.filter(id__in=liked_art_ids)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Art.objects.values_list('category', flat=True).distinct()

        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user).values_list('art_id', flat=True)
            context['user_likes'] = set(user_likes)

        return context
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
        
        # Afficher une page de confirmation
        context = {
            'art': art,
            'confirmation_message': f"Voulez-vous {'publier' if not art.is_public else 'mettre en privé'} cet art ?",
        }
        return render(request, 'confirm.html', context)

    def post(self, request, art_id):
        # Récupérer l'objet art
        art = get_object_or_404(Art, id=art_id)
        
        # Basculer l'état de is_public
        art.is_public = not art.is_public
        art.save()
        
        # Rediriger vers la liste des arts
        return redirect('list_arts')

class LikeArtView(View):
    def post(self, request, art_id):
        art = get_object_or_404(Art, id=art_id)
        user = request.user

        # Vérifie si le like existe
        like, created = Like.objects.get_or_create(user=user, art=art)


        if not created:
            # Si le like existe déjà, le supprime
            like.delete()
        else:
            # Si le like est nouveau, il est déjà enregistré avec `get_or_create`
            pass

        # Redirige vers la galerie
        return redirect('gallery')
    

    


