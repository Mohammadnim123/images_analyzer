from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SkinImage
from django.conf import settings


class BaseSerializer(serializers.Serializer):
    def is_valid(self):
        return super().is_valid(raise_exception=True)
    
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class SkinImageSerializer(serializers.Serializer):
    image_url = serializers.SerializerMethodField()
    description = serializers.CharField(max_length=99999999)

    def get_image_url(self, obj):
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/')
        image_path = obj.image.url.lstrip('/')
        return base_url + image_path
