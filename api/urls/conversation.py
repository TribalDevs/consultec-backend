from django.urls import path
from api.views.conversation import ConversationMessagesView, ConversationValidateView, ValidateConversationView, ConversationsView

urlpatterns = [
    path("active/", ConversationsView.as_view(), name="Conversation"),
    
    path("<str:convo_id>/messages/", ConversationMessagesView.as_view(), name="Conversation Messages"),

    path("<str:user_id>/new/", ValidateConversationView.as_view(), name="Post Message"),
    
    path("<str:user_id>/messages/", ConversationValidateView.as_view(), name="Validate Messages"),
]