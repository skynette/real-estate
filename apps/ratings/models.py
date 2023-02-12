from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel
from apps.profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class Rating(TimeStampedUUIDModel):

	class Range(models.IntegerChoices):
		RATING_1 = 1, _("Poor")
		RATING_2 = 2, _("Fair")
		RATING_3 = 3, _("Good")
		RATING_4 = 4, _("Very Good")
		RATING_5 = 5, _("Excellent")

	rater = models.ForeignKey(User, verbose_name="User providing rating", on_delete=models.SET_NULL, null=True)
	agent = models.ForeignKey(Profile, verbose_name="Agent to be rated", related_name="agent_review", on_delete=models.SET_NULL, null=True)
	rating = models.IntegerField(verbose_name="Rating", default=0, choices=Range.choices, help_text="1=Poor, 2=Fair 3=Good 4=Vey good 5=Excellent")
	comment = models.TextField(_("Comment"))

	class Meta:
		unique_together = ["rater", "agent"]

	def __str__(self) -> str:
		return f"{self.agent} rated at {self.rating}"