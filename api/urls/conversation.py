from django.urls import path
from api.views.conversation import ConversationMessagesView, ConversationValidateView, ValidateConversationView, ConversationsView

urlpatterns = [
    path("active/", ConversationsView.as_view(), name="Conversation"),
    
    path("validate/group/<str:convo_id>/", ConversationMessagesView.as_view(), name="Conversation Messages"),

    path("new/<str:user_id>/", ValidateConversationView.as_view(), name="Post Message"),
    
    path("validate/history/<str:user_id>/", ConversationValidateView.as_view(), name="Validate Messages"),
]