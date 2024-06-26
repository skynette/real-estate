from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    rater = serializers.SerializerMethodField(read_only=True)
    agent = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rating
        exclude = ["updated_at", "pk"]

    def get_rater(self, obj: Rating) -> str:
        return obj.rater.username

    def get_agent(self, obj: Rating) -> str:
        return obj.agent.user.username
