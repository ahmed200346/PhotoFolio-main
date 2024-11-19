from django.urls import path
from . import views

urlpatterns = [
path('checkout/<int:art_id>/', views.checkOut, name='checkout'),
path('payment-success/<int:art_id>/', views.paymentSuccessful, name='payment-success'),
path('payment-failed/<int:art_id>/', views.paymentFailed, name='payment-failed'),
]