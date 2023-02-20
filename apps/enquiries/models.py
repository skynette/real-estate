from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedUUIDModel

class Enquiry(TimeStampedUUIDModel):
	name = models.CharField(_("Your Name"), max_length=100)
	phone_number = PhoneNumberField(_("Your Phone Number"), max_length=30, default="+2348189999999")
	email = models.EmailField(_("Your Email"))
	subject = models.CharField(_("Subject"), max_length=100)
	message = models.TextField(_("Message"))

	def __str__(self) -> str:
		return f"{self.email}"

	class Meta:
		verbose_name_plural = "Enquiries"