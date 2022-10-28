from django.urls import path
from api.views.sign_up import SignUpView

urlpatterns = [
    path('', SignUpView.as_view())
]