from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .serializers import PropertySerializer
from .models import Property


# APIView alternative 1 to the function based view
class UpdatePropertyAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def put(self, request, slug, *args, **kwargs):
		property = Property.objects.filter(slug=slug).first()
		if not property: 
			raise PropertyNotFoundException
		user = getattr(request, 'user', None)
		if property.user != user:
			return Response({"error": "You can't update a property that doesn't belong to you."}, status=status.HTTP_403_FORBIDDEN)
		
		data = request.data
		serializer = PropertySerializer(property, data, many=False)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data, status=status.HTTP_200_OK)


# generics alternative 2 to the function based view
class UpdatePropertyAPIView(generics.UpdateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Property, slug=slug)
        return obj

    def perform_update(self, serializer):
        serializer.save()

# alternative 1 to function based view of creating property
class CreatePropertyAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		user = getattr(request, 'user', None)
		data = request.data
		data['user'] = user.pkid
		serializer = PropertyCreateSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			logger.info(
				f"Property {serializer.data.get('title')} created"
			)
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# alternative 2 using generics 
class CreatePropertyAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertyCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info(f"Property {serializer.data.get('title')} created")


# alternative 1 to delete
class DeletePropertyAPIView(generics.DestroyAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"
    queryset = Property.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = getattr(request, 'user', None)
        if instance.user != user:
            return Response({"error": "You can't delete a property that doesn't belong to you."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


# alternative 2 to delete
class DeletePropertyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
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

# alt 1
class UploadPropertyImageAPIView(APIView):
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

#alt 2
class UploadPropertyImageAPIView(generics.CreateAPIView):
    serializer_class = PropertySerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        property_id = data["property_id"]
        property = Property.objects.filter(id=property_id).first()
        serializer = self.get_serializer(property, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Image(s) uploaded successfully"}, status=status.HTTP_201_CREATED)


#alternative property search views

class PropertyFilter(filters.FilterSet):
    price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    bedrooms = filters.NumberFilter(field_name="bedrooms", lookup_expr='gte')
    # Add more filters for other fields as needed

    class Meta:
        model = Property
        fields = ['advert_type', 'property_type', 'price', 'bedrooms']
        
class PropertySearchAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter
    
    def get_queryset(self):
        queryset = Property.objects.filter(published_status=True)
        return queryset

