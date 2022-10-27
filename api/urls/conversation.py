from django.urls import path
from api.views.conversation import ValidateConversationView

urlpatterns = [
    path("", ValidateConversationView.as_view(), name="Search User"),
]