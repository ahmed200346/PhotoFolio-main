from django import forms
from .models import Art
from django.core.exceptions import ValidationError

from django import forms
from django.core.exceptions import ValidationError
from .models import Art

class AddArt(forms.ModelForm):
    class Meta:
        model = Art
        fields = ['title', 'category', 'price', 'tags', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Entrez un titre'}),
            'category': forms.TextInput(attrs={'placeholder': 'Entrez une catégorie'}),
            'tags': forms.Textarea(attrs={'placeholder': 'Entrez des tags'}),
            'description': forms.Textarea(attrs={'placeholder': 'Entrez une description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise ValidationError("Le prix doit être supérieur à zéro.")
        return price


class UpdateArt(forms.ModelForm):
    class Meta:
        model = Art
        fields = ['title', 'category', 'price', 'tags', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Entrez un titre'}),
            'category': forms.TextInput(attrs={'placeholder': 'Entrez une catégorie'}),
            'tags': forms.Textarea(attrs={'placeholder': 'Entrez des tags'}),
            'description': forms.Textarea(attrs={'placeholder': 'Entrez une description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre tous les champs obligatoires
        for field_name, field in self.fields.items():
            field.required = True

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise ValidationError("Le prix doit être supérieur à zéro.")
        return price