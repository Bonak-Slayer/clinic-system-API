from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Clinic, Message, User
from .serializers import ClinicSerializer, MessageSerializer

# Create your views here.
@api_view(['GET'])
def index(request):
    all_clinics = Clinic.objects.all()
    serialize_clinics = ClinicSerializer(all_clinics, many=True)
    return Response({'clinics': serialize_clinics.data}, 200)

@api_view(['GET'])
def get_clinic(request, clinic_id):
    try:
        clinic = Clinic.objects.get(id=clinic_id)
        serialize_clinic = ClinicSerializer(clinic)
        return Response({'clinic': serialize_clinic.data}, 200)
    except:
        return Response({'error': 'No Clinic Found'}, 204)

@api_view(['GET'])
def get_inbox(request, user):
    current_user = User.objects.get(username=user)
    inbox = Message.objects.filter(recipient_id=current_user.id)
    serialize_inbox = MessageSerializer(inbox, many=True)
    return Response({'inbox': serialize_inbox.data}, 200)