from django import forms
from .models import Art
from django.core.exceptions import ValidationError

class AddArt(forms.ModelForm):
    class Meta:
        model = Art
        fields = ['title', 'category', 'price', 'tags', 'description', 'file']
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise ValidationError("Le prix doit être supérieur à zéro.")
        return price

class UpdateArt(forms.ModelForm):
    class Meta:
        model = Art  
        fields = ['title', 'category', 'price', 'tags', 'description']
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise ValidationError("Le prix doit être supérieur à zéro.")
        return price