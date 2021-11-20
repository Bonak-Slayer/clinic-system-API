from django.contrib import admin
from .models import Clinic, Staff, Category, Inquiry, Appointment, Message, Expertise, Role

# Register your models here.
admin.site.register(Clinic)
admin.site.register(Expertise)
admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(Category)
admin.site.register(Inquiry)
admin.site.register(Appointment)
admin.site.register(Message)