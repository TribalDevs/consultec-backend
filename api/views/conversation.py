from rest_framework.views import APIView
from api.models import Conversation, ConversationMessage, ConversationUser, TechUser
from api.serializers.user import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

class ValidateConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            initiator = TechUser.objects.get(id=request.user.id)
            receiver = TechUser.objects.get(id=pk)

            if initiator == receiver:
                return Response({"error": "You cannot send a message to yourself"}, status=status.HTTP_400_BAD_REQUEST)
            
            conversation = Conversation.objects.filter(
                Q(conversationuser__user=initiator) & Q(conversationuser__user=receiver)
            ).first()

            if not conversation:
                conversation = Conversation.objects.create()
                convo_initiator = ConversationUser(conversation=conversation, user=initiator)
                convo_receiver = ConversationUser(conversation=conversation, user=receiver)
                convo_list = [convo_initiator, convo_receiver]
                ConversationUser.objects.bulk_create(convo_list)
            
            new_message = ConversationMessage.objects.create(
                conversation = conversation,
                user = initiator,
                message = request.data["message"]
            )
            return Response({"message": "Message sent successfully"}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class SearchUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            user_id = request.user.id
            item = TechUser.objects.filter(
                (
                    Q(first_name__icontains=data["query"])
                    | Q(last_name__icontains=data["query"])
                    | Q(email__icontains=data["query"])
                    | Q(identifier_number__icontains=data["query"])
                )
                & ~Q(id=user_id)
            )
            serializer = UserSerializer(item, many=True)
            return Response({"users": serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
