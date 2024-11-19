from django.db import models
from django.core.validators import EmailValidator

# Create your models here.


class Admin_actor(models.Model):
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    cin = models.CharField(max_length=8)
    email = models.EmailField(validators=[EmailValidator])
    password = models.CharField(max_length=20)
    post = models.CharField(max_length=20)
    VIP_statue = models.BooleanField()