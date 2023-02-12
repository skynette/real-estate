from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('supersecret/', admin.site.urls),
    path('api/v1/auth/', include('apps.authentication.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Real Estate Admin"
admin.site.site_title = "Real estate Admin Portal"
admin.site.index_title = "Welcome to the Real estate portal"
