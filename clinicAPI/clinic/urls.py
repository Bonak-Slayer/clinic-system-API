from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clinic/<int:clinic_id>', views.get_clinic, name='clinic'),
    path('messages/<str:user>', views.get_inbox, name='inbox')
]