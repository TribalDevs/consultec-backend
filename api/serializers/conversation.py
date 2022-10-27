from django.contrib.auth.models import UserManager
from rest_framework import serializers
from api.serializers.user import UserSerializer
from api.models import Conversation, ConversationMessage, ConversationUser, TechUser
from django.db.models import Q


class ConversationMessageSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = "__all__"

    def get_user(self, obj):
        user = TechUser.objects.get(id=obj.user.id)
        return UserSerializer(user).data


class ConversationUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ConversationUser
        fields = "__all__"

    def get_user(self, obj):
        receiver = ConversationUser.objects.filter(
            Q(conversation=obj.conversation) & ~Q(user=obj.user)
        ).values_list("user")
        receiver = TechUser.objects.filter(id__in=receiver)
        return UserSerializer(receiver, many=True).data
