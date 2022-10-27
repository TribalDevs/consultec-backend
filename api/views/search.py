from rest_framework.views import APIView
from api.models import TechUser
from api.serializers.user import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


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
