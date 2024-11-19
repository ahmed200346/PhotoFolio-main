from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import re
def only_Letters(value):
    if not re.match(r'^[a-zA-Z\s]+$', value):
        raise ValidationError('Ce champ ne doit contenir que des lettres et des espaces.')
def Email_Valide(value):
    if not value.endswith("@gmail.com") and not value.endswith("@esprit.tn"):
        raise ValidationError("Adresse mail doit etre @gmail ou @esprit")
class User(AbstractUser):
    biography = models.TextField(blank=True, null=True,help_text="Une brève biographie ou description")
    first_name = models.CharField(max_length=30, validators=[only_Letters])
    last_name = models.CharField(max_length=30, validators=[only_Letters])
    email = models.EmailField(unique=True,validators=[Email_Valide])
    username = models.CharField(max_length=50, unique=True)
    USERNAME_FIELD="username"
    is_artist = models.BooleanField(default=False, help_text="Indique si l'utilisateur est un artiste")
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        verbose_name = "User"
