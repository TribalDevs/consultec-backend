from rest_framework.views import APIView
from api.models import Conversation, ConversationMessage, ConversationUser, TechUser
from api.serializers.user import UserSerializer
from api.serializers.conversation import (
    ConversationMessageSerializer,
    ConversationUserSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class AdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        try:
            user = TechUser.objects.all()
            serializer = UserSerializer(user, many=True)
            return Response({"message": serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class AdminValidateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def put(self, request, user_id):
        try:
            user = TechUser.objects.get(id=user_id)
            
            if not user.is_validated:
                user.is_validated = True
                user.save()
            return Response({"message": "User validated"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)