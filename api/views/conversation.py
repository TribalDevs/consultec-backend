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
from rest_framework.permissions import IsAuthenticated


class ConversationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = TechUser.objects.get(id=request.user.id)
            convos = ConversationUser.objects.filter(user=user)
            serializer = ConversationUserSerializer(convos, many=True)
            return Response({"message": serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class ConversationMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, convo_id):
        try:
            user = request.user.id
            convo = Conversation.objects.filter(
                Q(id=convo_id) & Q(conversationuser__user=user)
            )
            if convo.exists():
                messages = ConversationMessage.objects.filter(conversation=convo[0])
                serializer = ConversationMessageSerializer(messages, many=True)
                return Response({"message": serializer.data}, status.HTTP_200_OK)
            return Response(
                {"error": "You are not a member of this conversation"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class ValidateConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            data = request.data
            initiator = TechUser.objects.get(id=request.user.id)
            receiver = TechUser.objects.get(id=user_id)

            if initiator == receiver:
                return Response(
                    {"error": "You cannot send a message to yourself"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            conversation = Conversation.objects.filter(
                Q(conversationuser__user=initiator) & Q(conversationuser__user=receiver)
            ).first()

            if not conversation:
                conversation = Conversation.objects.create()
                convo_initiator = ConversationUser(
                    conversation=conversation, user=initiator
                )
                convo_receiver = ConversationUser(
                    conversation=conversation, user=receiver
                )
                convo_list = [convo_initiator, convo_receiver]
                ConversationUser.objects.bulk_create(convo_list)

            new_message = ConversationMessage.objects.create(
                conversation=conversation, user=initiator, message=data["message"]
            )
            return Response(
                {
                    "message": "Message sent successfully",
                    "conversation": conversation.id,
                },
                status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
