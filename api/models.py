from multiprocessing.sharedctypes import Value
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from api.utils.upload import get_file_path
from django.utils import timezone

# Create your models here.
ADMINISTRATOR = 1
COLLABORATOR = 2
STUDENT = 3

MALE = 'male'
FEMALE = 'female'
NOT_ESPECIFIED = 'not_especified'


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

    ROLES_CHOICES = (
        (ADMINISTRATOR, 'Administrator'),
        (COLLABORATOR, 'Collaborator'),
        (STUDENT, 'Student')
    )

    id = models.UUIDField(_("id(uuid)"),primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, blank=True)
    email = models.EmailField(_("email"), max_length=60, unique=True)
    role = models.PositiveIntegerField(_("user role"), default=STUDENT, choices=ROLES_CHOICES)
    is_validated = models.BooleanField(_("is validated user"),default=False)
    identifier_number = models.PositiveIntegerField(_("user id number"), unique=True)
    profile_picture = models.ImageField(_("user picture"), default=None, upload_to=get_file_path)



    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NOT_ESPECIFIED, 'Not especified')
    )

    gender = models.CharField(_('user gender'), max_length=15, default=NOT_ESPECIFIED, choices=GENDER_CHOICES)
    
    # The following fields are required for every custom User model
    username = None
    last_login = models.DateTimeField(_('last login'), auto_now=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'identifier_number']

    objects = TechUserManager()

    def __str__(self):
        return str(self.identifier_number)

class Conversation(models.Model):
    id = models.UUIDField(_("id(uuid)"),primary_key=True, default=uuid.uuid4, editable=False)
    total_messages = models.PositiveIntegerField(_("total messages"), default=0)

    def __str__(self):
        return str(self.id)

class ConversationUser(models.Model):
    id = models.UUIDField(_("id(uuid)"),primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(TechUser, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return str(self.id)

class ConversationMessage(models.Model):
    id = models.UUIDField(_("id(uuid)"),primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(TechUser, on_delete=models.CASCADE)
    message = models.TextField(_("message"), max_length=2000)
    created_at = models.DateTimeField(_("created at"), default=timezone.now)

    def __str__(self):
        return str(self.id)