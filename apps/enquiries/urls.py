from django.urls import path
from . import views

urlpatterns = [
    path('', views.send_enquiry_email_view, name='send_enquiry_view')
]
