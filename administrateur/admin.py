from django.contrib import admin
from .models import Admin_actor
# Register your models here.



@admin.register(Admin_actor)
class Admin_actor_display(admin.ModelAdmin):
    pass