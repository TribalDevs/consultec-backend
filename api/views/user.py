from rest_framework.views import APIView
from api.models import TechUser
from api.serializers.user import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = TechUser.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response({"message": serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        try:
            data = request.data
            if str(request.user.id) == str(user_id):
                user = TechUser.objects.get(id=user_id)
                user.first_name = data["first_name"]
                user.last_name = data["last_name"]
                if data["profile_picture"] != "" and data["profile_picture"] != None:
                    user.profile_picture = data["profile_picture"]
                user.save()
                serializer = UserSerializer(user)
                return Response({"message": serializer.data}, status.HTTP_200_OK)
            return Response(
                {"error": "You are not authorized to perform this action"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)