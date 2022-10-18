from distutils.command.sdist import sdist
from ossaudiodev import SOUND_MIXER_CD
from ssl import ALERT_DESCRIPTION_DECODE_ERROR
from stat import SF_APPEND
from django.urls import path
from api.views.sign_up import SignUpView

urlpatterns = [
    path('new/', SignUpView.as_view())
]