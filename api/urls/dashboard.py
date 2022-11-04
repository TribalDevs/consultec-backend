from django.urls import path
from api.views.dashboard import AdminView, AdminValidateView

urlpatterns = [
    path("users/", AdminView.as_view(), name="Search Users"),
    path("validate/<str:user_id>/", AdminValidateView.as_view(), name="Validate User"),
]