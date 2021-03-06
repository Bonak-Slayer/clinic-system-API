from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Clinic(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=11)
    email = models.EmailField()
    operation_start = models.TimeField()
    operation_end = models.TimeField()
    starting_day = models.CharField(max_length=9)
    end_day = models.CharField(max_length=9)
    description = models.CharField(max_length=800)

    def __str__(self):
        return f"{self.name}'s details"


#STAFF RELATED CLASSES#
class Expertise(models.Model):
    field = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.field}'

class Role(models.Model):
    active_role = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.active_role}'

class Staff(models.Model):
    assigned_clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='assigned_clinic')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='job')
    specialization = models.ManyToManyField(Expertise, blank=True)

    def __str__(self):
        return f'{self.role} {self.user.first_name} {self.user.last_name} of {self.assigned_clinic.name}'



#APPOINTMENT AND INTERACTIVITY RELATED CLASSES#
class Category(models.Model):
    patient_category = models.CharField(max_length=25)


class Inquiry(models.Model):
    content = models.CharField(max_length=1500)
    date = models.DateTimeField(auto_now=True)
    inquirer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquirer')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='inquired_clinic')

    def __str__(self):
        return f"{self.inquirer}'s inquiry for {self.clinic}"

class Appointment(models.Model):
    appointment_date = models.DateTimeField()
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='assigned_doctor')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='appointment_clinic')

class Message(models.Model):
    content = models.CharField(max_length=800)
    date = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')

    def __str__(self):
        return f"{self.sender} said '{self.content}' to {self.recipient}"
