from django import forms

from .models import Admin_actor


class Admin_actor_forms(forms.ModelForm):
    class Meta:
        models = Admin_actor
        fields = '_all_'
