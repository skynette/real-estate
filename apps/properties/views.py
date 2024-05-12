import logging

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from .exceptions import PropertyNotFoundException
from .models import Property, PropertyViews
from .pagination import PropertyPagination
from .serializers import PropertySerializer, PropertyViewsSerializer, PropertyCreateSerializer

logger = logging.getLogger(__name__)


class PropertyFilter(django_filters.FilterSet):
    advert_type = django_filters.CharFilter(field_name="advert_type", lookup_expr="iexact")
    property_type = django_filters.CharFilter(field_name="property_type", lookup_expr="iexact")
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    price__lt = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Property
        fields = ["advert_type", "property_type", "price"]


class ListAllPropertyAPIView(generics.ListAPIView):
    """Get all properties."""
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by("-created_at")
    pagination_class = PropertyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

    @extend_schema(
        description="Retrieve a list of all properties",
        responses={
            200: PropertySerializer(many=True),
            400: "Bad request",
            500: "Internal server error"
        },
        tags=["properties"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


list_all_property_api_view = ListAllPropertyAPIView.as_view()


class ListAgentsPropertyAPIView(generics.ListAPIView):
    """Get properties for specific user or agents."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

    @extend_schema(
        description="Retrieve properties for a specific user or agents.",
        responses={
            200: PropertySerializer(many=True),
            400: "Bad request",
            500: "Internal server error",
        },
        tags=["properties"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        qs = Property.objects.filter(user=user).order_by("-created_at")
        return qs


list_agents_property_api_view = ListAgentsPropertyAPIView.as_view()


class PropertyViewsAPIView(generics.ListAPIView):
    serializer_class = PropertyViewsSerializer
    queryset = PropertyViews.objects.all()

    @extend_schema(
        description="Retrieve all property views.",
        responses={200: PropertyViewsSerializer(many=True)},
        tags=["properties"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


property_views_api_view = PropertyViewsAPIView.as_view()


class PropertyDetailViewsAPIView(generics.GenericAPIView):
    serializer_class = PropertySerializer

    @extend_schema(
        description="Retrieve a property detail",
        responses={
            200: PropertySerializer,
            400: "Bad request",
            500: "Internal server error"
        },
        tags=["properties"]
    )
    def get(self, request, slug, *args, **kwargs):
        property = Property.objects.get(slug=slug)

        # checking if request coming from proxy server to get the ip address
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(":")[0]
        # gets the ip address from remote address
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not PropertyViews.objects.filter(property=property, ip=ip).exists():
            PropertyViews.objects.create(property=property, ip=ip)
            property.views += 1
            property.save()

        serializer = self.get_serializer(property, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


property_detail_api_view = PropertyDetailViewsAPIView.as_view()


class UpdatePropertyAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySerializer

    @extend_schema(
        description="Update a property",
        request=PropertySerializer,
        responses={
            200: PropertySerializer,
            400: "Bad request",
            500: "Internal server error"
        },
        tags=["properties"]
    )
    def put(self, request, slug, *args, **kwargs):
        property = Property.objects.filter(slug=slug).first()
        if not property:
            raise PropertyNotFoundException
        user = getattr(request, 'user', None)
        if property.user != user:
            return Response({"error": "You can't update a property that doesn't belong to you."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        serializer = self.get_serializer(property, data, many=False, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


update_property_api_view = UpdatePropertyAPIView.as_view()


class CreatePropertyAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertyCreateSerializer

    @extend_schema(
        description="Create a property",
        request=PropertyCreateSerializer,
        responses={
            200: PropertyCreateSerializer,
            400: "Bad request",
            500: "Internal server error"
        },
        tags=["properties"]
    )
    def post(self, request):
        user = getattr(request, 'user', None)
        data = request.data
        data['user'] = user.pkid
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"Property {serializer.data.get('title')} created"
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


create_property_api_view = CreatePropertyAPIView.as_view()


class DeletePropertyAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySerializer

    @extend_schema(
        description="Delete a property",
        responses={
            200: PropertySerializer,
            400: "Bad request",
            500: "Internal server error"
        },
        tags=["properties"]
    )
    def delete(self, request, slug, format=None):
        property = Property.objects.filter(slug=slug).first()
        if not property:
            raise PropertyNotFoundException
        user = getattr(request, 'user', None)
        if property.user != user:
            return Response({"error": "You can't delete a property that doesn't belong to you."}, status=status.HTTP_403_FORBIDDEN)
        delete_operation = property.delete()
        data = {}
        if delete_operation:
            data["success"] = "Deleted successfully"
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data["failure"] = "Deletion failed"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


delete_property_api_view = DeletePropertyAPIView.as_view()


class UploadPropertyImageAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    @extend_schema(
        description="Upload property images",
        responses={
            201: {"success": "Image(s) uploaded successfully"},
            400: "Bad request",
            500: "Internal server error"
        },
        tags=["properties"]
    )
    def post(self, request, *args, **kwargs):
        data = request.data
        property_id = data["property_id"]
        property = Property.objects.filter(id=property_id).first()
        property.cover_photo = request.FILES.get("cover_photo", None)
        property.photo1 = request.FILES.get("photo1", None)
        property.photo2 = request.FILES.get("photo2", None)
        property.photo3 = request.FILES.get("photo3", None)
        property.photo4 = request.FILES.get("photo4", None)
        property.save()
        return Response({"success": "Image(s) uploaded successfully"}, status=status.HTTP_201_CREATED)


upload_property_image_api_view = UploadPropertyImageAPIView.as_view()


class PropertySearchFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    bedrooms = django_filters.NumberFilter(field_name="bedrooms", lookup_expr='gte')
    # Add more filters for other fields as needed

    class Meta:
        model = Property
        fields = ['advert_type', 'property_type', 'price', 'bedrooms']


class PropertySearchAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertySearchFilter

    def get_queryset(self):
        queryset = Property.objects.filter(published_status=True)
        return queryset


property_search_api_view = PropertySearchAPIView.as_view()
