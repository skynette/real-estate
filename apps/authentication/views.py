from apps.authentication.serializers import LoginSerializer, RegistrationSerializer
from apps.authentication.utils import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import generics, status
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class CustomTokenObtainPairView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="User login successful",
                response=LoginSerializer
            ),
            400: OpenApiResponse(description="Bad request", response=LoginSerializer),
            500: OpenApiResponse(description="Internal server error"),
        },
        description="Login a user",
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = TokenObtainPairSerializer.get_token(user)

            return Response({
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'email': user.email,
                },
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'message': 'User Login successfully',
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


login_view = CustomTokenObtainPairView.as_view()
