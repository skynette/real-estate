from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
	"""
	Custom user model manager where email is the unique identifiers
	for authentication instead of usernames.
	"""
	def email_validator(self, email):
		try:
			validate_email(email)
		except ValidationError:
			raise ValueError(_("You must provide a valid email address"))

	def create_user(self, username, first_name, last_name, email, password, **extra_fields):
		"""
		Create and save a User with the given email and password.
		"""
		if not username:
			raise ValueError(_("Users must submit a usernmae"))
		
		if not first_name:
			raise ValueError(_("users must submit first name"))	
		
		if not last_name:
			raise ValueError(_("users must submit last name"))	
		
		if not email:
			raise ValueError(_('The Email must be set'))

		if email:
			email = self.normalize_email(email)
			self.email_validator(email)
		else:
			raise ValueError(_("Base user account: An email is required"))

		user = self.model(username=username, first_name=first_name, last_name=last_name, email=email, **extra_fields)
		user.set_password(password)
		
		# neccessary?
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		user.save()
		return user

	def create_superuser(self, username, first_name, last_name, email, password, **extra_fields):
		"""
		Create and save a SuperUser with the given email and password.
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		if not password:
			raise ValueError(_('Superuser must have password'))
		if email:
			email = self.normalize_email(email)
			self.email_validator(email)
		else:
			raise ValueError(_("Admin account: An email is required"))
		
		
		return self.create_user(username, first_name, last_name, email, password, **extra_fields)