from django.db import models
from django.core.validators import EmailValidator
from users.models import User
from arts.models import Art,Like
class Admin(User):
    POST_CHOICES = (
        ('Art', 'Art'),
        ('Users', 'Users'),
        ('Paiement', 'Paiement'),
        ('Admin', 'Admin'),
    )
    VIP_Status = models.BooleanField(default=False)  
    post = models.CharField(max_length=20, choices=POST_CHOICES, default='Admin')  
    def __str__(self):
        return f"Admin: {self.user.username}, Role: {self.post}, VIP: {self.VIP_Status}"
    @property
    def is_active(self):
        return super().is_active and (self.VIP_Status or self.post != 'Admin')
