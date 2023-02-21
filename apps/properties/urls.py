from django.urls import path
from . import views

urlpatterns = [
	path("all/", views.list_all_property_api_view, name="all_properties"),
]
