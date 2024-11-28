from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import PasswordResetForm
def validate_biography(value):
    max_length = 500
    forbidden_words = ['spam', 'fake', 'banned']
    if len(value) > max_length:
        raise ValidationError(f"La biographie ne peut pas dépasser {max_length} caractères.")
    for word in forbidden_words:
        if word in value.lower():
            raise ValidationError(f"La biographie contient un mot interdit : '{word}'.")
    return value


# Validation pour les noms
def validate_only_letters(value):
    if not re.match(r'^[a-zA-Z\s]+$', value):
        raise ValidationError("Ce champ ne doit contenir que des lettres et des espaces.")


# Validation pour l'adresse email
def validate_email(value):
    if not value.endswith("@gmail.com") and not value.endswith("@esprit.tn"):
        raise ValidationError("L'adresse email doit se terminer par @gmail.com ou @esprit.tn.")
    return value


# Validation pour le nom d'utilisateur
def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError("Le nom d'utilisateur ne peut contenir que des caractères alphanumériques et des underscores (_).")
    if User.objects.filter(username=value).exists():
        raise ValidationError("Ce nom d'utilisateur est déjà pris.")
    return value


# Formulaire d'inscription
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'biography', 'is_artist', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['biography'].validators.append(validate_biography)
        self.fields['first_name'].validators.append(validate_only_letters)
        self.fields['last_name'].validators.append(validate_only_letters)
        self.fields['email'].validators.append(validate_email)
        self.fields['username'].validators.append(validate_username)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hash le mot de passe
        if commit:
            user.save()
        return user
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'biography']

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.instance.username: 
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username
class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail n'est pas enregistrée.")
        return email

