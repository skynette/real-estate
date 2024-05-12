from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # Optional UI:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    path('supersecret/', admin.site.urls),
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/profile/', include('apps.profiles.urls')),
    path('api/v1/properties/', include('apps.properties.urls')),
    path('api/v1/ratings/', include('apps.ratings.urls')),
    path('api/v1/enquiries/', include('apps.enquiries.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Real Estate Admin"
admin.site.site_title = "Real estate Admin Portal"
admin.site.index_title = "Welcome to the Real estate portal"
