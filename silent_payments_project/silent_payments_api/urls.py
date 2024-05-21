
from django.urls import path
from . import views

urlpatterns = [
    path('generate-silent-payment-address/', views.generate_silent_payment, name='generate_silent_payment_address'),
]