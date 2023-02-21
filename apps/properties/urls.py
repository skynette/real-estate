from django.urls import path
from . import views

urlpatterns = [
    path("all/", views.list_all_property_api_view, name="all_properties"),
    path("agents/", views.list_agents_property_api_view, name="agent_properties"),
    path("create/", views.create_property_api_view, name="create_property"),
    path("details/<slug:slug>/", views.property_detail_api_view, name="details"),
    path("update/<slug:slug>/", views.update_property_api_view, name="update_property"),
    path("delete/", views.delete_property_api_view, name="delete_property"),
    path("search/", views.property_search_api_view, name="search_property"),
]
