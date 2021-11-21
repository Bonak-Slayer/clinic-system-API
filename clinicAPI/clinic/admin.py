from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ClinicUser, Clinic, Staff, Inquiry, Appointment, Message, Expertise, Role

# Register your models here.
admin.site.register(ClinicUser)
admin.site.register(Clinic)
admin.site.register(Expertise)
admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(Inquiry)
admin.site.register(Appointment)
admin.site.register(Message)