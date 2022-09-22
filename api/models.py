from multiprocessing.sharedctypes import Value
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

ADMINISTRATOR = 1
PERSONNEL = 2
STUDENT = 3

ROLES = (
    (ADMINISTRATOR, 'Administrator'),
    (PERSONNEL, 'Personnel'),
    (STUDENT, 'Student')
)

class TechUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', ADMINISTRATOR)

        if extra_fields.get('role') is not ADMINISTRATOR:
            raise ValueError(_("Superuser must be an ADMINISTRATOR"))
        return self.create_user(email, password, **extra_fields)

class TechUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email"), max_length=60, unique=True)
    role = models.PositiveIntegerField(_("user role"), default=STUDENT)
    is_validated = models.BooleanField(default=False)


    # The following fields are required for every custom User model
    username = None
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = TechUserManager()

    def __str__(self):
        return self.email