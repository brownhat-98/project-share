from django.conf import settings
from rest_framework import serializers
from .models import Destination

class destination_serializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True,required=False)
    class Meta:
        model = Destination
        fields = '__all__'

