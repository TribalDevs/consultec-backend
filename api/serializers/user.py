from django.contrib.auth.models import UserManager
from rest_framework import serializers
from api.models import TechUser

class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TechUser
        fields = ['id', 'email', 'identifier_number' ,'first_name', 'last_name', 'gender', 'role', 'profile_picture']

    def get_role(self, obj):
        return obj.get_role_display()