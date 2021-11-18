from django.contrib import admin
from .models import Clinic, Staff, Category, Inquiry, Appointment, Message

# Register your models here.
admin.site.register(Clinic)
admin.site.register(Staff)
admin.site.register(Category)
admin.site.register(Inquiry)
admin.site.register(Appointment)
admin.site.register(Message)