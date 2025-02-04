from django.urls import path
from .views import premium_payment

urlpatterns = [
    path('premium/', premium_payment, name='premium_payment'),
    # Outras URLs do seu projeto
]