import random
import string

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries import CountryField
from apps.common.models import TimeStampedUUIDModel

User = get_user_model()

class PropertyPublishedManager(models.Manager):
	def get_queryset(self):
		return super(PropertyPublishedManager, self).get_queryset().filter(published_status=True)


class Property(TimeStampedUUIDModel):
	class AdvertType(models.TextChoices):
		FOR_SALE = "For Sale", _('For Sale')
		FOR_RENT = "For Rent", _('For rent')
		AUCTION = "Auction", _('Auction')

	class PropertyType(models.TextChoices):
		HOUSE = "House", _('House')
		APARTMENT = "Apartment", _('Apartment')
		OFFICE = "Office", _('Office')
		WAREHOUSE = "Warehouse", _('Warehouse')
		COMMERCIAL = "Commercial", _("Commercial")
		OTHER = "Other", _("Other")
	
	user = models.ForeignKey(User, verbose_name=_("Agent, Seller or Buyer"), related_name="agent_buyer", on_delete=models.DO_NOTHING)
	title = models.CharField(verbose_name=_("Property Title"), max_length=255)
	slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
	ref_code = models.CharField(verbose_name=_("Property Ref Code"), max_length=255, unique=True, blank=True, null=True)
	description = models.TextField(_("Description"), blank=True, default="Default description")
	country = CountryField(_("Country"), blank=True, default="NG", blank_label="(select country)")
	city = models.CharField(_("City"), max_length=255, default="Lagos")
	postal_code = models.CharField(_("Postal Code"), max_length=255, default="140")
	street_address = models.CharField(_("Street Address"), max_length=255, default="Street Address")
	property_number = models.IntegerField(_("Property Number"), validators=[MinValueValidator(1)], default=112)
	price = models.DecimalField(_("Price"), max_digits=8, decimal_places=2, default=0.0)
	plot_area = models.DecimalField(_("Plot Area"), decimal_places=2, max_digits=8, default=0.0)
	bedrooms = models.IntegerField(_("bedrooms"), default=1)
	bathrooms = models.IntegerField(_("bathrooms"), default=1)
	advert_type = models.CharField(_("Advert Type"), max_length=255, choices=AdvertType.choices, default=AdvertType.FOR_SALE)
	property_type = models.CharField(_("Property Type"), max_length=255, choices=PropertyType.CHOICES, default=PropertyType.OTHER)
	cover_photo = models.ImageField(_("Main Photo"))
	



