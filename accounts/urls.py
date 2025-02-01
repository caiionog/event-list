from django.urls import path
from .views import register, user_login, logout_view, verify_email

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
]
