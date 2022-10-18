from django.urls import path
from api.views.login import MyTokenObtainPairView
# from base.views.refreshToken import CustomTokenRefreshView

urlpatterns = [
    path("", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
]