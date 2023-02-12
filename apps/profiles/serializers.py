from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from apps.ratings.serializers import RatingSerializer
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
	username = serializers.CharField(source="user.username")
	first_name = serializers.CharField(source="user.first_name")
	last_name = serializers.CharField(source="user.last_name")
	email = serializers.EmailField(source="user.email")
	full_name = serializers.SerializerMethodField(readonly=True)
	country = CountryField(name_only=True)
	reveiews = serializers.SerializerMethodField(readonly=True)

	class Meta:
		model = Profile
		exclude = ["pkid"]

	def get_full_name(self, obj):
		first_name = obj.user.first_name.title()
		last_name = obj.user.last_name.title()
		return f"{first_name} {last_name}"

	def get_reviews(self, obj):
		reviews = obj.agent_review.all()
		serializer = RatingSerializer(reviews, many=True)
		return serializer.data

	def to_representation(self, instance):
		representation = super().to_representation(instance)
		if instance.top_agent:
			representation['top_agent'] = True
		return representation

