import logging

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

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

# view to list all properties


class ListAllPropertyAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by("-created_at")
    pagination_class = PropertyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]


list_all_property_api_view = ListAllPropertyAPIView.as_view()

# view to list all properties for a given agent


class ListAgentsPropertyAPIView(generics.ListAPIView):
    """Get properties for specific user or agents."""
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = getattr(self.request, 'user', None)
        return super().filter(user=user).order_by("-created_at")


list_agents_property_api_view = ListAgentsPropertyAPIView.as_view()

# view to get the number of views for a property


class PropertyViewsAPIView(generics.ListAPIView):
    serializer_class = PropertyViewsSerializer
    queryset = PropertyViews.objects.all()


property_views_api_view = PropertyViewsAPIView.as_view()

# view to get property details


class PropertyDetailViewsAPIView(APIView):

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

        serializer = PropertySerializer(property, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


property_detail_api_view = PropertyDetailViewsAPIView.as_view()

# view to update property details


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_property_api_view(request, slug):
    property = Property.objects.filter(slug=slug).first()
    if not property:
        raise PropertyNotFoundException
    user = getattr(request, 'user', None)
    if property.user != user:
        return Response({"error": "You can't update a property that doesn't belong to you."}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    serializer = PropertySerializer(property, data, many=False)
    serializer.valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

# view to create a new property


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_property_api_view(request):
    user = getattr(request, 'user', None)
    data = request.data
    data['user'] = user.pkid
    serializer = PropertyCreateSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"Property {serializer.data.get('title')} created"
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# view to delete a property


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_property_api_view(request, slug):
    property = Property.objects.filter(slug=slug).first()
    if not property:
        raise PropertyNotFoundException
    user = getattr(request, 'user', None)
    if property.user != user:
        return Response({"error": "you can't delete a property that is not yours"}, status=status.HTTP_403_FORBIDDEN)
    delete_operation = property.delete()
    data = {}
    if delete_operation:
        data["success"] = "Deleted successfully"
        return Response(data, status=status.HTTP_202_ACCEPTED)
    else:
        data["failure"] = "Deletion failed"
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

# view to upload images for a specific property


@api_view(["POST"])
def upload_property_image_api_view(request):
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

# view to search for properties with different criteria


class PropertySearchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySerializer

    def post(self, request, *args, **kwargs):
        queryset = Property.objects.filter(published_status=True)
        data = self.request.data

        advert_type = data['advert_type']
        queryset = queryset.filter(advert_type__iexact=advert_type)

        property_type = data['property_type']
        queryset = queryset.filter(property_type__iexact=property_type)

        price = data['price']
        if price == "$0+":
            price = 0
        elif price == "$50,000+":
            price = 50000
        # go on till 600,000
        elif price == "Any":
            price = -1

        if price != -1:
            queryset = queryset.filter(price__gte=price)

        bedrooms = data["bedrooms"]
        if bedrooms == "0+":
            bedrooms = 0
        # go on till 5
        elif bedrooms == "Any":
            bedrooms = -1
        queryset = queryset.filter(bedrooms__gte=bedrooms)

        # do same for bathrooms

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


property_search_api_view = PropertySearchAPIView.as_view()
