from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

class TimeStampedUUIDModel(models.Model):
	pkid = models.BigAutoField(_("primary key id"), primary_key=True, editable=False)
	id = models.UUIDField(_("Id"), default=uuid.uuid4, editable=False, unique=True)
	created_at = models.DateTimeField(_("Created"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Updated"), auto_now=True)

	class Meta:
		abstract = True