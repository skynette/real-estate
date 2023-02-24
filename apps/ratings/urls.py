from django.urls import path

from . import views

urlpatterns = [
	path("<str:profile_id>/", views.create_agent_review_optimized, name="create_rating")
]
