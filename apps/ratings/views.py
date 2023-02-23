from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Avg

from apps.profiles.models import Profile
from .models import Rating

User = get_user_model()

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_agent_review(request, profile_id):
	agent_profile = Profile.objects.get(id=profile_id, is_agent=True)
	data = request.data

	profile_user = User.objects.get(pkid=agent_profile.user.pkid)
	if profile_user.email == request.user.email:
		return Response({"message": "Cannot rate yourself"}, status=status.HTTP_403_FORBIDDEN)

	already_exists = agent_profile.agent_review.filter(agent__pkid=profile_user.pkid).exists()
	if already_exists:
		content = {
			"detail": "Profile already reviewed"
		}
		return Response(content, status=status.HTTP_403_FORBIDDEN)
	
	elif data["rating"] == 0:
		return Response({"message":"please provide a rating"}, status=status.HTTP_400_BAD_REQUEST)
	
	review = Rating.objects.create(rater=request.user, agent=agent_profile, rating=data["rating"], comment=data["comment"])
	reviews = agent_profile.agent_review.all()
	agent_profile.num_reveiews = reviews.count()
	total = 0
	for i in reviews:
		total += i.rating

	return Response({"message":"Reviewed successfully"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_agent_review_optimized(request, profile_id):
	try:
		agent_profile = Profile.objects.get(id=profile_id, is_agent=True)
	except Profile.DoesNotExist:
		return Response({"message": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

	if agent_profile.user.email == request.user.email:
		return Response({"message": "Cannot rate yourself"}, status=status.HTTP_403_FORBIDDEN)

	data = request.data
	rating = data.get("rating", None)
	comment = data.get("comment", None)

	if rating is None or rating == 0:
		return Response({"message":"Please provide a rating"}, status=status.HTTP_400_BAD_REQUEST)

	if agent_profile.agent_review.filter(rater=request.user).exists():
		return Response({"detail": "You already reviewed this agent's profile"}, status=status.HTTP_403_FORBIDDEN)

	Rating.objects.create(rater=request.user, agent=agent_profile, rating=rating, comment=comment)
	agent_profile.num_reviews = agent_profile.agent_review.count()
	agent_profile.average_rating = agent_profile.agent_review.aggregate(avg_rating=Avg('rating'))['avg_rating']
	agent_profile.save()

	return Response({"message": "Review created successfully"}, status=status.HTTP_201_CREATED)
