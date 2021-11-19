from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('clinic/<int:clinic_id>', views.get_clinic, name='clinic'),
    path('messages/<str:user>', views.get_inbox, name='inbox'),
    path('sendMessage', views.receive_message, name='receive')
]