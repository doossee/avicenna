from random import randint
from datetime import date

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

from solo.models import SingletonModel
from imagekit import models as ik_models, processors as ik_processors 

from .choices import *
from .managers import UserManager
from .services.tasks import send_password, send_verify_code


class User(AbstractUser, PermissionsMixin):

    """Main user"""

    avatar = models.ImageField(verbose_name=_("Avatar"), upload_to="avatars/", default=settings.NO_AVATAR)
    phone = models.CharField(verbose_name=_("Phone Number"), max_length=15, unique=True)

    middle_name = models.CharField(verbose_name=_("Middle name"), max_length=50, blank=True)
    birth_date = models.DateField(verbose_name=_("Birth date"), default=date(2000, 1, 1), blank=True)

    verify_code = models.PositiveSmallIntegerField(verbose_name=_("Verify Code"), default=0)
    verify_time = models.DateTimeField(verbose_name=_("Verify Time"), default=timezone.now)

    created_at = models.DateTimeField(verbose_name=_("Created Time"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated Time"), auto_now=True)

    user_type = models.CharField(verbose_name=_("User type"), max_length=10, choices=UserTypeChoices.choices)

    email = None
    groups = None
    user_permissions = None

    objects = UserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "user"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def save(self, *args, **kwargs):
        self.user_type = self.get_user_type()
        self.username = self.phone
        super().save(*args, **kwargs)

    def get_user_type(self):
        if isinstance(self, Doctor):
            return "DOCTOR"
        elif isinstance(self, Patient):
            return "PATIENT"
        elif isinstance(self, Admin):
            return "ADMIN"
        else:
            return self.user_type

    def change_password(self, password, new_password, confirm_password):
        """ """
        if not self.check_password(password):
            raise ValidationError(_("Password is incorrect!"))

        if new_password != confirm_password:
            raise ValidationError(_("New password and confirmation password are equal!"))

        self.set_password(confirm_password)
        super().save()

    def reset_password(self):
        password = randint(100000, 999999)
        self.set_password(str(password))
        super().save()
        return send_password.delay(self.phone, password)

    def change_avatar(self, avatar):
        self.avatar = avatar
        super().save()

    def generate_verify_code(self):
        code = randint(1000, 9999)
        self.is_active = False
        self.verify_code = code
        self.verify_time = timezone.now() + timezone.timedelta(minutes=settings.VERIFY_CODE_MINUTES)
        return send_verify_code.delay(self.phone, code)

    def regenerate_verify_code(self):
        result = self.generate_verify_code()
        super().save()
        return result

    def verify(self, code):
        if self.verify_code == code and self.verify_time >= timezone.now():
            self.is_active = True
            super().save()
            return True
        return False


class Admin(User, SingletonModel):

    """Admin user model"""

    singleton_instance_id = 2

    class Meta:
        db_table = "admin"
        verbose_name = _("Admin")


class Doctor(User):

    """Doctor user model"""

    specialties = models.ManyToManyField(verbose_name=_("Specialty"), to="Specialty", blank=True, related_name="doctors")

    experience = models.IntegerField(verbose_name=_("Experience"), null=True, blank=True)
    experiences = models.TextField(verbose_name=_("Experiences"), blank=True)
    
    work_time_start = models.TimeField(_("Start time of work")) 
    work_time_end = models.TimeField(_("End time of work")) 

    schedule = models.CharField(_("Schedule"), max_length=255)
    
    licences = models.TextField(verbose_name=_("Licences"), blank=True)
    educations = models.TextField(verbose_name=_("Educations"), blank=True)
    certificates = models.TextField(verbose_name=_("Certificates"), blank=True)

    rating = models.DecimalField(verbose_name=_("Rating"), max_digits=3, decimal_places=2)
    
    is_published = models.BooleanField(verbose_name=_("Publish"), default=True)
    
    class Meta:
        db_table = "doctor"
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")


class Patient(User):

    """Patient user model"""

    class Meta:
        db_table = "patient"
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")


class Specialty(models.Model):

    """Specialty model"""
    
    name = models.CharField(verbose_name=_("Name"), max_length=150)

    class Meta:
        verbose_name = _("Specialty")
        verbose_name_plural = _("Specialties")


# class Chat(models.Model):
    
#     """Chat model"""
    
#     users = models.ManyToManyField(verbose_name=_("Chat users"), to=User, related_name='chats')
#     is_open = models.BooleanField(verbose_name=_("Is chat open"), default=True)
#     created_at = models.DateTimeField(verbose_name=_("Create date"), auto_now_add=True)
#     updated_at = models.DateTimeField(verbose_name=_("Update date"), auto_now=True)

#     class Meta:
#         verbose_name = _("Chat")
#         verbose_name_plural = _("Chats")

        
# class ChatMessage(models.Model):

#     """Chat message model"""

#     sender = models.ForeignKey(
#         verbose_name=_("Message sender"), to=User, 
#         on_delete=models.CASCADE, related_name='messages'
#     )
#     chat = models.ForeignKey(
#         verbose_name=_("Chat"), to=Chat, 
#         on_delete=models.CASCADE, related_name='messages'
#     )
#     message = models.TextField(verbose_name=_("Message"))
#     is_viewed = models.BooleanField(verbose_name=_("Is message viewed"), default=False)
#     created_at = models.DateTimeField(verbose_name=_("Create date"), auto_now_add=True)
#     updated_at = models.DateTimeField(verbose_name=_("Update date"), auto_now=True)

         
