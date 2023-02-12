import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.profiles.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		logger.info("User Profile created")
