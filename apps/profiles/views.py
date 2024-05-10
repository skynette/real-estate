from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .exceptions import ProfileNotFoundException, NotYourProfileException
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer

from drf_spectacular.utils import extend_schema


class AgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer


agent_list_api_view = AgentListAPIView.as_view()


class TopAgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(top_agent=True)
    serializer_class = ProfileSerializer


top_agent_list_api_view = TopAgentListAPIView.as_view()


class GetProfileAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = ProfileSerializer

    @extend_schema(
        description="Retrieve the profile of the authenticated user",
        responses={
            200: ProfileSerializer,
            401: "Unauthorized",
            404: "Not Found",
        },
        tags=["profiles"]
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = Profile.objects.get(user=user)
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


get_profile_api_view = GetProfileAPIView.as_view()


class UpdateProfileAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    @extend_schema(
        description="Update the profile of the authenticated user",
        parameters=[
            {
                "name": "username",
                "required": True,
                "in": "path",
                "type": "string",
                "description": "The username of the user to update"
            }
        ],
        request=UpdateProfileSerializer,
        responses={
            200: UpdateProfileSerializer,
            401: "Unauthorized",
            404: "Not Found",
        },
        tags=["profiles"]
    )
    def patch(self, request, username, *args, **kwargs):
        try:
            Profile.objects.get(user__username=username)
        except:
            raise ProfileNotFoundException

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfileException

        data = request.data
        serializer = self.serializer_class(instance=request.user.profile, data=data, partial=True)

        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


update_profile_api_view = UpdateProfileAPIView.as_view()
