from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()

class Gender(models.TextChoices):
	MALE = "Male", _("Male")
	FEMALE = "Female", _("Female")
	OTHER = "Other", _("Other")

class Profile(TimeStampedUUIDModel):
	user = models.OneToOneField(User, verbose_name=_("User model"), related_name="profile", on_delete=models.CASCADE)
	phone_number = PhoneNumberField(verbose_name=_("Phone number"), max_length=20, default="+234980000000")
	bio = models.TextField(_("About Me"), default="something about yourself")
	license = models.CharField(_("Real State License"), max_length=50, blank=True, null=True)
	profile_photo = models.ImageField(_("Profile Photo"),default="/profile_default.png")
	gender = models.CharField(_("Gender"), max_length=50, choices=Gender.choices, default=Gender.OTHER)
	country = CountryField(_("Country"), default="NG", blank=False, null=False)
	city = models.CharField(_("City"), max_length=50, null=False, blank=False)
	is_buyer = models.BooleanField(_("IsBuyer"), default=False, help_text="Are you looking to buy")
	is_seller = models.BooleanField(_("IsSeller"), default=False, help_text="Are you looking to sell")
	is_agent = models.BooleanField(_("IsAgent"), default=False, help_text="Are you an agent?")
	top_agent = models.BooleanField(_("TopAgent"), default=False)
	rating = models.DecimalField(_("Rating"), max_digits=4, decimal_places=2, null=True, blank=True)
	num_reviews = models.IntegerField(_("Number of Reveiews"), default=0, null=True, blank=True)

	class Meta:
		verbose_name = _("Profile")
		verbose_name_plural = _("Profiles")

	def __str__(self):
		return f"{self.user.username}'s profile"
	