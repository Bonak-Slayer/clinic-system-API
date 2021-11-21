from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ClinicUser, Clinic, Staff, Message, Appointment
from .serializers import ClinicSerializer, MessageSerializer, ClinicUserSerializer, StaffSerializer, AppointmentSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        all_clinics = Clinic.objects.all()
        serialize_clinics = ClinicSerializer(all_clinics, many=True)
        return Response({'clinics': serialize_clinics.data}, 200)

    elif request.method == 'POST':
        clinic = request.POST.get('search')
        searched_clinics = Clinic.objects.filter(name__contains=clinic)
        serialize_search = ClinicSerializer(searched_clinics, many=True)
        return Response({'clinics': serialize_search.data}, 200)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = ClinicUser.objects.get(email=email)
            if user.password == password:
                serialize_user = ClinicUserSerializer(user)
                print('\n\nSUCCESSFULLY AUTHENTICATED USER')

            print(serialize_user.data)
            return Response({'message': 'LOGIN SUCCESS', 'user_data': serialize_user.data}, 200)
        except:
            return Response({'message': 'LOGIN FAILED'})


@api_view(['GET'])
def get_clinic(request, clinic_id):
    try:
        clinic = Clinic.objects.get(id=clinic_id)
        serialize_clinic = ClinicSerializer(clinic)

        staff = Staff.objects.filter(assigned_clinic__name__exact=clinic.name)
        serialize_staff = StaffSerializer(staff, many=True)

        return Response({'clinic': serialize_clinic.data, 'staff': serialize_staff.data}, 200)
    except:
        return Response({'error': 'No Clinic Found'}, 204)



@api_view(['GET'])
def get_inbox(request, user):
    current_user = ClinicUser.objects.get(username=user)
    inbox = Message.objects.filter(recipient_id=current_user.id)
    serialize_inbox = MessageSerializer(inbox, many=True)
    return Response({'inbox': serialize_inbox.data}, 200)



@api_view(['POST'])
def receive_message(request):
    if request.method == 'POST':
        try:
            sender = request.POST.get('sender')
            recipient = request.POST.get('recipient')
            message = request.POST.get('content')

            verify_sender = ClinicUser.objects.get(email=sender)
            verify_recipient = ClinicUser.objects.get(email=recipient)
            newMessage = Message(sender=verify_sender, recipient=verify_recipient, content=message)
            newMessage.save()

            print(newMessage)
            return Response({'message': 'message received'}, 200)
        except:
            return Response({'message': 'message failed'}, 200)

@api_view(['POST'])
def make_appointment(request):
    if request.method == 'POST':
        try:
            category = request.POST.get('patientCategory')
            doctor = request.POST.get('doctor')
            has_symptoms = request.POST.get('healthCheck')
            vaccinated = request.POST.get('vaccinationCheck')
            patient = request.POST.get('patient')
            clinic = request.POST.get('clinic')

            requestedDoctor = Staff.objects.get(id=doctor)
            requestedPatient = ClinicUser.objects.get(id=patient)
            requestedClinic = Clinic.objects.get(id=clinic)

            symptom_check = False
            vaccination_check = False
            if has_symptoms == 'yes':
                symptom_check = True

            elif vaccinated == 'yes':
                vaccination_check = True


            appointment = Appointment(appointment_status="Pending",
                                      patient=requestedPatient,
                                      category=category,
                                      doctor=requestedDoctor,
                                      clinic=requestedClinic,
                                      health_check=symptom_check,
                                      vaccinated=vaccination_check)
            appointment.save()

            return Response({'message': 'appointment created'}, 200)
        except:
            return Response({'message': 'appointment failed'}, 200)

@api_view(['GET'])
def get_appointments(request, user):
    if request.method == 'GET':
        try:
            user = ClinicUser.objects.get(id=user)

            appointments = Appointment.objects.filter(patient=user)
            appointment_serializer = AppointmentSerializer(appointments, many=True)

            return Response({'message': 'retrieved', 'appointments': appointment_serializer.data}, 200)
        except:
            return Response({'message': 'failed to get appointments'}, 200)