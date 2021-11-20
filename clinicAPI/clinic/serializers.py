from rest_framework import serializers
from .models import Clinic, Staff, Message
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'contact', 'email', 'operation_start', 'operation_end',
                  'starting_day', 'end_day', 'description']

class StaffSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    role = serializers.StringRelatedField()
    specialization = serializers.StringRelatedField(many=True)

    class Meta:
        model = Staff
        fields = ['user', 'role', 'specialization']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'date', 'sender', 'recipient']
