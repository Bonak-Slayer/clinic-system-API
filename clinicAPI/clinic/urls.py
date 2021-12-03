from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('clinic/<int:clinic_id>', views.get_clinic, name='clinic'),
    path('messages/<str:user>', views.get_inbox, name='inbox'),
    path('sentmessages/<str:user>', views.get_sent, name='sent'),
    path('sendMessage', views.receive_message, name='receive'),
    path('appointment', views.make_appointment, name='appointment'),
    path('getAppointments/<str:user>', views.get_appointments, name='all-appointments'),
    path('makeInquiry', views.make_inquiry, name='inquiry'),
    path('staff/allclinics/<str:staff_id>', views.assigned_clinics, name='assigned')
]