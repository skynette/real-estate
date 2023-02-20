from rest_framework import serializers
from .models import Enquiry

class EnquirySerializer(serializers.ModelSerializer):
	class Meta:
		model = Enquiry
		field = "__all__"

