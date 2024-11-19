from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'biography', 'is_artist']  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hash le mot de passe
        if commit:
            user.save()
        return user
    

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username','biography']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username
