from django.urls import path
from . import views

urlpatterns = [
	path('me/', views.get_profile_api_view, name="get_profile"),
	path('update/<str:username>/', views.update_profile_api_view, name="update_profile"),
	path('agents/all/', views.agent_list_api_view, name="all_agents"),
	path('top-agents/all/', views.top_agent_list_api_view, name="top_agents"),
	
]

