from django.core.mail import send_mail
from .serializers import EnquirySerializer

from zcore.settings.development import DEFAULT_FROM_EMAIL
from rest_framework import permissions, status, generics
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.utils import OpenApiResponse


class SendEnquiryEmailView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnquirySerializer

    @extend_schema(
        request=EnquirySerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={'application/json'},
                description="Enquiry was successfully submitted",
                examples=[
                    OpenApiExample(
                        name="Enquiry was successfully submitted",
                        value={
                            "success": "Enquiry was successfully submitted"
                        }
                    )
                ]
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={'application/json'},
                description="Bad request",
                examples=[
                    OpenApiExample(
                        name="Bad request",
                        value={
                            "error": "Bad request"
                        }
                    )
                ]
            )
        },
        tags=["Enquiries"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.send_email(serializer.validated_data)
        serializer.save()
        return Response({"success": "Enquiry was successfully submitted"}, status=status.HTTP_200_OK)

    def send_email(self, validated_data):
        subject = validated_data.get('subject')
        message = validated_data.get('message')
        from_email = validated_data.get('email')
        recipient_list = [DEFAULT_FROM_EMAIL]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)


send_enquiry_email_view = SendEnquiryEmailView.as_view()
