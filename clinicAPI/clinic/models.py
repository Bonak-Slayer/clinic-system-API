from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class ClinicUser(AbstractUser):
    middle_name = models.CharField(max_length=200)
    contact = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    sex = models.CharField(max_length=6)
    user_category = models.CharField(max_length=10)
    offense_count = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

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
        return f"{self.name}"


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
    user = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='staff')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='job')
    specialization = models.ManyToManyField(Expertise, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'



#APPOINTMENT AND INTERACTIVITY RELATED CLASSES#
class Inquiry(models.Model):
    content = models.CharField(max_length=3000)
    date = models.DateTimeField(auto_now=True)
    inquirer = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='inquirer')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='inquired_clinic')

    def __str__(self):
        return f"{self.inquirer}'s inquiry for {self.clinic}"

class Appointment(models.Model):
    appointment_date = models.DateTimeField(blank=True, null=True)
    appointment_status = models.CharField(max_length=32)
    patient = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='patient')
    category = models.CharField(max_length=32)
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='assigned_doctor')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='appointment_clinic')
    health_check = models.BooleanField()
    vaccinated = models.BooleanField()

    def __str__(self):
        return f"Appointment for {self.patient} at {self.clinic}, to be conducted by {self.doctor}"

class Message(models.Model):
    content = models.CharField(max_length=800)
    date = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='recipient')

    def __str__(self):
        return f"Message sent by: {self.sender}, sent to {self.recipient}"

class Notification(models.Model):
    recipient = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='notificationRecipient')
    dateReceived = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=120)

    def __str__(self):
        return f'Notification for {self.recipient}, received {self.dateReceived}'


