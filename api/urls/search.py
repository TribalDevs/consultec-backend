from django.urls import path
from api.views.search import SearchUserView
# from base.views.refreshToken import CustomTokenRefreshView

urlpatterns = [
    path("", SearchUserView.as_view(), name="Search User"),
]