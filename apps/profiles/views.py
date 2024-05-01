from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import ProfileNotFoundException, NotYourProfileException
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer


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


class GetProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


get_profile_api_view = GetProfileAPIView.as_view()


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

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
