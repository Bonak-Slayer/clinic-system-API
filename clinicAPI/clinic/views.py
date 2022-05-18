import datetime
from .cluster import create_analysis
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ClinicUser, Clinic, Staff, Message, Appointment, Inquiry, Notification, Expertise, Role

from .serializers import \
    ClinicSerializer, \
    MessageSerializer, \
    ClinicUserSerializer, \
    StaffSerializer, \
    AppointmentSerializer, \
    NotificationSerializer, \
    ExpertiseSerializer, \
    RoleSerializer


# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        all_clinics = Clinic.objects.all()
        serialize_clinics = ClinicSerializer(all_clinics, many=True)
        return Response({'clinics': serialize_clinics.data}, 200)

    elif request.method == 'POST':
        clinic = request.POST.get('search')

        if clinic == "":
            searched_clinics = Clinic.objects.all()
        else:
            searched_clinics = Clinic.objects.filter(name__contains=clinic)

        serialize_search = ClinicSerializer(searched_clinics, many=True)
        return Response({'clinics': serialize_search.data}, 200)


@api_view(['POST'])
def signup(request):
    firstName = request.POST.get('firstName')
    middleName = request.POST.get('middleName')
    lastName = request.POST.get('lastName')
    password = request.POST.get('password')
    sex = request.POST.get('sex')
    email = request.POST.get('email')
    address = request.POST.get('address')
    contact = request.POST.get('contact')
    birthDate = request.POST.get('birthDate')

    try:
        clinicUser = ClinicUser.objects.create_user(username=firstName,
                                                    first_name=firstName,
                                                    middle_name=middleName,
                                                    last_name=lastName,
                                                    email=email,
                                                    sex=sex,
                                                    address=address,
                                                    contact=contact,
                                                    user_category='Staff',
                                                    offense_count=0)
        clinicUser.set_password(password)
        print(clinicUser)
        clinicUser.save()
        return Response({'message': 'sign up success'}, 200)
    except:
        return Response({'message': 'sign up failed'}, 200)

@api_view(['POST'])
def staff_signup(request):
    firstName = request.POST.get('firstName')
    middleName = request.POST.get('middleName')
    lastName = request.POST.get('lastName')
    password = request.POST.get('password')
    sex = request.POST.get('sex')
    email = request.POST.get('email')
    address = request.POST.get('address')
    contact = request.POST.get('contact')
    birthDate = request.POST.get('birthDate')
    specializations = request.POST.get('specializations')
    role = request.POST.get('role')

    individualized = specializations.split(",")

    try:
        clinicUser = ClinicUser.objects.create_user(username=firstName,
                                                    first_name=firstName,
                                                    middle_name=middleName,
                                                    last_name=lastName,
                                                    email=email,
                                                    sex=sex,
                                                    address=address,
                                                    contact=contact,
                                                    user_category='Staff',
                                                    offense_count=0)
        clinicUser.set_password(password)
        clinicUser.save()

        # CREATION OF STAFF
        getRole = Role.objects.get(active_role__contains=role)
        print(role)
        newStaff = Staff(user=clinicUser, role=getRole)
        newStaff.save()

        for specialization in individualized:
            equivalent = Expertise.objects.get(field__iexact=specialization)
            newStaff.specialization.add(equivalent)

        newStaff.save()
        return Response({'message': 'sign up success'}, 200)
    except:
        return Response({'message': 'sign up failed'}, 200)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = ClinicUser.objects.get(email=email)
            if user.check_password(password):
                serialize_user = ClinicUserSerializer(user)
                print('\n\nSUCCESSFULLY AUTHENTICATED USER')

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
    current_user = ClinicUser.objects.get(id=user)
    inbox = Message.objects.filter(recipient_id=current_user.id)

    serialize_inbox = MessageSerializer(inbox, many=True)
    return Response({'inbox': serialize_inbox.data}, 200)

@api_view(['GET'])
def get_sent(request, user):
    current_user = ClinicUser.objects.get(id=user)
    sent = Message.objects.filter(sender=current_user)

    serialize_sent = MessageSerializer(sent, many=True)
    return Response({'sent': serialize_sent.data}, 200)


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
            appointment = request.POST.get('appointmentDate')
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

            print(appointment)

            appointment = Appointment(appointment_date=appointment,
                                      appointment_status="Pending",
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
    try:
        user = ClinicUser.objects.get(id=user)

        appointments = Appointment.objects.filter(patient=user)
        appointment_serializer = AppointmentSerializer(appointments, many=True)

        return Response({'message': 'retrieved', 'appointments': appointment_serializer.data}, 200)
    except:
        return Response({'message': 'failed to get appointments'}, 200)


@api_view(['POST'])
def make_inquiry(request):
    user = request.POST.get('user')
    clinic = request.POST.get('clinic')
    content = request.POST.get('content')

    retrieved_user = ClinicUser.objects.get(id=user)
    retrieved_clinic = Clinic.objects.get(id=clinic)

    try:
        newInquiry = Inquiry(inquirer=retrieved_user, clinic=retrieved_clinic, content=content)
        newInquiry.save()
        return Response({'message': 'inquiry success'}, 200)
    except:
        return Response({'message': 'inquiry failed!'}, 200)

#STAFF ENDPOINTS
@api_view(['GET'])
def assigned_clinics(request, staff_id):
    user = ClinicUser.objects.get(id=staff_id)
    staff = Staff.objects.get(user=user)


    clinics = staff.assigned_clinic.all()
    serialize_clinics = ClinicSerializer(clinics, many=True)

    return Response({'clinics': serialize_clinics.data}, 200)

@api_view(['GET'])
def get_staff(request, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)
    staff = Staff.objects.filter(assigned_clinic=clinic)

    serialize_staff = StaffSerializer(staff, many=True)
    return Response({'staff': serialize_staff.data}, 200)

@api_view(['GET'])
def get_clinic_appointments(request, clinic_id):
    clinic = Clinic.objects.get(id=clinic_id)
    appointments = Appointment.objects.filter(clinic=clinic)

    serialize_appointments = AppointmentSerializer(appointments, many=True)
    return Response({'appointments': serialize_appointments.data}, 200)

@api_view(['POST'])
def handle_appointment(request, appt_id):
    status = request.POST.get('status')

    appointment = Appointment.objects.get(id=appt_id)
    appointment.appointment_status = status

    if(status == 'Approved'):
        time = request.POST.get('time')

        getDate = f'{appointment.appointment_date.date()} {time}'
        approvedDateTime = datetime.datetime.strptime(getDate, '%Y-%m-%d %H:%M')

        appointment.appointment_date = approvedDateTime
        appointment.save()

        approved_notification = Notification(recipient=appointment.patient,
                                             content=f'APPROVED: {appointment}')
        approved_notification.save()
        create_analysis(appointment.clinic.name)
        return Response({'message': 'Appointment successfully approved.'}, 200)

    elif(status == 'Rejected'):
        reject_notification = Notification(recipient=appointment.patient,
                                             content=f'REJECTED: {appointment}')
        reject_notification.save()

        appointment.save()
        return Response({'message': 'Appointment successfully rejected.'}, 200)

    #HANDLING OF CANCELLATION OF APPOINTMENTS
    elif (status == 'cancelApproved'):
        appointment.appointment_status = 'Cancelled'
        reject_notification = Notification(recipient=appointment.patient,
                                           content=f'CANCELLATION APPROVED: {appointment}')
        reject_notification.save()

        appointment.save()
        return Response({'message': 'Appointment successfully cancelled.'}, 200)

    elif (status == 'cancelRejected'):
        appointment.appointment_status = 'Cancellation Request Rejected'
        reject_notification = Notification(recipient=appointment.patient,
                                           content=f'CANCELLATION REJECTED: {appointment}')
        reject_notification.save()

        appointment.save()
        return Response({'message': 'Appointment cancellation was rejected.'}, 200)


@api_view(['POST'])
def reschedule_appointment(request, appt_id):
    reschedule_date = request.POST.get('rescheduleDate')

    appointment = Appointment.objects.get(id=appt_id)
    appointment.appointment_date = datetime.datetime.strptime(reschedule_date, '%Y-%m-%d %H:%M')
    appointment.appointment_status = 'Requested for Reschedule'
    appointment.save()

    return Response({'message': 'reschedule request sent'}, 200)


@api_view(['POST'])
def cancel_appointment(request):
    appointment_id = request.POST.get('appointment')

    appointment = Appointment.objects.get(id=appointment_id)
    appointment.appointment_status = 'Requested for Cancellation'
    appointment.save()

    return Response({'message': 'cancellation request sent'}, 200)


@api_view(['GET'])
def get_notifications(request, user_id):
    user = ClinicUser.objects.get(id=user_id)
    notifications = Notification.objects.filter(recipient=user)

    serialize_notifications = NotificationSerializer(notifications, many=True)
    return Response({'notifications': serialize_notifications.data}, 200)


@api_view(['GET'])
def get_clinic_duties(request):
    specializations = Expertise.objects.all()
    serialize_expertise = ExpertiseSerializer(specializations, many=True)

    roles = Role.objects.all()
    serialize_roles = RoleSerializer(roles, many=True)

    return Response({'message': 'expertise retrieval success',
                     'specializations': serialize_expertise.data,
                     'roles': serialize_roles.data}, 200)

@api_view(['POST'])
def register_clinic(request):
    user_id = request.POST.get('user')
    name = request.POST.get('name')
    address = request.POST.get('address')
    contact = request.POST.get('contact')
    email = request.POST.get('email')
    operation_start = request.POST.get('opStart')
    operation_end = request.POST.get('opEnd')
    starting_day = request.POST.get('dayStart')
    end_day = request.POST.get('dayEnd')
    description = request.POST.get('description')

    user = ClinicUser.objects.get(id=user_id)
    clinics = Clinic.objects.all()
    for clinic in clinics:
        if clinic.name.casefold() == name.casefold():
            return Response({'message': 'clinic registration failed'}, 200)

    newClinic = Clinic(name=name,
                       address=address,
                       contact=contact,
                       email=email,
                       operation_start=operation_start,
                       operation_end=operation_end,
                       starting_day=starting_day,
                       end_day=end_day,
                       description=description)
    newClinic.save()

    staffMember = Staff.objects.get(user=user)
    staffMember.assigned_clinic.add(newClinic)
    staffMember.save()
    return Response({'message': 'successfully registered clinic'}, 200)

@api_view(['POST'])
def associate(request):
    user_id = request.POST.get('user')
    clinic_id = request.POST.get('clinic')

    user = ClinicUser.objects.get(id=user_id)
    clinic = Clinic.objects.get(id=clinic_id)
    staffMember = Staff.objects.get(user=user)

    if clinic not in staffMember.assigned_clinic.all():
        staffMember.assigned_clinic.add(clinic)
        staffMember.save()
        return Response({'message': 'association successful'}, 200)
    else:
        return Response({'message': 'you are already part of this clinic'}, 200)


