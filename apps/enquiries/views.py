from django.core.mail import send_mail

from zcore.settings.development import DEFAULT_FROM_EMAIL
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Enquiry

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def send_enquiry_email(request):
	data = request.data 
	try:
		subject = data.get('subject')
		name = data.get('name')
		email = data.get('email')
		message = data.get('message')
		from_email = data.get('from_email')
		recipient_list = [DEFAULT_FROM_EMAIL]
		
		send_mail(subject, message, from_email, recipient_list, fail_silently=True)
		
		enquiry = Enquiry.objects.create(name=name, email=email, subject=subject, message=message)
		enquiry.save()
		
		return Response({"success": "Enquiry was successfully submitted"}, status=status.HTTP_200_OK)
	except:
		return Response({"error": "Enquiry could not be submitted"}, status=status.HTTP_400_BAD_REQUEST)


