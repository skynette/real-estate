from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
import uuid


class User(AbstractUser):
	pkid = models.BigAutoField(_("primary key id"), primary_key=True, editable=False)
	id = models.UUIDField(_("Id"), default=uuid.uuid4, editable=False, unique=True)
	email = models.EmailField(_('email address'), unique=True)
	username = models.CharField(_('username'), max_length=50, blank=True, null=True, unique=True)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	objects = CustomUserManager()

	class Meta:
		verbose_name = _('User')
		verbose_name_plural = _('Users')

	def __str__(self):
		return f"{self.username}"

	@property
	def get_full_name(self) -> str:
		return f"{self.first_name.title()} {self.last_name.title()}"
	
	def get_short_name(self) -> str:
		return f"{self.username}"
