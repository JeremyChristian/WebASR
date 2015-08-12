from django.db import models
from server import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
import os.path
""" UPLOAD MODEL """


class Upload(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='upload', )
    audiofiles = models.FileField(upload_to='storage/audiofiles')
    language = models.CharField(max_length=50)
    systems = models.CharField(max_length=50)
    transcripts = models.FileField(upload_to='storage/transcripts',)
    metadata = models.FileField(upload_to='storage/metadata')
    environment = models.CharField(max_length=50)
    status =  models.CharField(max_length=50, default='Processing...')

    def update_filename(self):
        path = "storage/audiofiles/"
        format = 'hello.me'
        return os.path.join(path, format)


    class meta:
    	odering = ('created')


""" SYSTEM MODEL """


class System(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    environment = models.CharField(max_length=50)
    command = models.CharField(max_length=200)
    # test_file = models.FileField()

    class meta:
        odering = ('added')


""" USER MODEL """


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=False,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
  
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])