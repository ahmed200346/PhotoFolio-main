from django.urls import path
from . import views

urlpatterns = [
    path('analyze_comment/', views.analyze_comment, name='analyze_comment'),
    path('analyze_file/', views.analyze_file, name='analyze_file'),
]
