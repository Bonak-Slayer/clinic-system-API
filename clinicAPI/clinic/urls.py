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
    path('rescheduleAppointment/<str:appt_id>', views.reschedule_appointment, name='reschedule_appointment'),
    path('cancelAppointment', views.cancel_appointment, name='cancel_appointment'),
    path('getAppointments/<str:user>', views.get_appointments, name='all-appointments'),
    path('getNotifications/<str:user_id>', views.get_notifications, name='notifications'),
    path('makeInquiry', views.make_inquiry, name='inquiry'),
    path('staff/allclinics/<str:staff_id>', views.assigned_clinics, name='assigned'),
    path('staff/allclinics/getClinic/<str:clinic_id>', views.get_staff, name='staff'),
    path('staff/clinic/appointments/<str:clinic_id>', views.get_clinic_appointments, name='clinic_appointments'),
    path('staff/clinic/appointments/approveAppointment/<str:appt_id>', views.handle_appointment, name='approve'),
]