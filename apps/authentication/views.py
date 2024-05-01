from rest_framework_simplejwt.views import TokenObtainPairView
from apps.authentication.serializers import MyTokenObtainPairSerializer, RegistrationSerializer
from apps.authentication.utils import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse

User = get_user_model()


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    @extend_schema(
        request=RegistrationSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="User account created successfully",
                response=RegistrationSerializer
            ),
            400: OpenApiResponse(description="Bad request", response=RegistrationSerializer),
            500: OpenApiResponse(description="Internal server error"),
        },
        description="Register a new user account",
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.data['username']
            user = User.objects.get(username=username)
            tokens = get_tokens_for_user(user)
            return Response({"user": serializer.data, "auth": tokens}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


registration_view = RegistrationAPIView.as_view()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


login_view = MyTokenObtainPairView.as_view()
