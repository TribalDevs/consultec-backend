from django.urls import path
from api.views.sign_up import SignUpView, SignUpAdminView

urlpatterns = [
    path('', SignUpView.as_view()),
    path('admin/', SignUpAdminView.as_view()),
]