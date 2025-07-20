from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework import serializers
from app.models import Project


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProjectSerializer(serializers.ModelSerializer):
    investors = serializers.StringRelatedField(many=True)  # shows __str__ of Investor

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'investors', 'location',
            'amount_required', 'amount_raised', 'start_date', 'end_date',
            'category', 'status', 'is_active', 'document', 'created_at'
        ]
