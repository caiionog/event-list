from django.urls import path
from . import views

app_name = 'feed'  # Namespace do app

urlpatterns = [
    path('', views.index, name='index'),  # URL raiz para a página inicial
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('report_message/<int:message_id>/', views.report_message, name='report_message'),
]