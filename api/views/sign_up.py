from rest_framework.views import APIView
from api.models import TechUser
from api.serializers.sign_up import SignUpSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File
import urllib.request
from rest_framework_simplejwt.tokens import RefreshToken

image_url = "https://res.cloudinary.com/dt4b5tkwd/image/upload/v1666084085/dev/default-profile-picture1_ypxtk1.jpg"
result = urllib.request.urlretrieve(image_url, 'TechUser/default.jpg')


DEFAULT_PROFILE_PICTURE = File(open(result[0], "rb"))


class SignUpView(APIView):
    def post(self, request):
        data = request.data

        serializer = SignUpSerializer(data=data, many=False)
        if serializer.is_valid():
            USER_EMAIL = data["email"]
            USER_PASSWORD = data["password"]
            new_user = TechUser.objects.create_user(
                email=USER_EMAIL,
                password=USER_PASSWORD,
                identifier_number=data["identifier_number"],
                profile_picture=DEFAULT_PROFILE_PICTURE,
                first_name=data["first_name"],
                last_name=data["last_name"],
                gender=data["gender"],
            )
            refresh = RefreshToken.for_user(new_user)
            return Response(
                {"message": "Sign up successful", "user": serializer.data, "access":str(refresh.access_token)},
                status.HTTP_201_CREATED,
            )
        return Response({"error": serializer.errors}, status.HTTP_400_BAD_REQUEST)
