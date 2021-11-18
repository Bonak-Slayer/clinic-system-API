from rest_framework import serializers
from .models import Clinic, Message

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'contact', 'email', 'operation_start', 'operation_end',
                  'starting_day', 'end_day', 'description']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'date', 'sender', 'recipient']