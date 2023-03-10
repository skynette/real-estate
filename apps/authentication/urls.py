from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from django.urls import path
from . import views

urlpatterns = [
	path('register/', views.registration_view, name='register_view'),
	path('login/', views.login_view, name='login_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]