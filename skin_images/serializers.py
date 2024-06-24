from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Articles


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'dob', 'gender']
        extra_kwargs = {'password': {'write_only': True}}


class SkinImageSerializer(serializers.Serializer):
    image_url = serializers.SerializerMethodField()
    description = serializers.CharField(max_length=99999999)

    def get_image_url(self, obj):
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/')
        image_path = obj.image.url.lstrip('/')
        return base_url + image_path


class ArticlesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Articles
        fields = '__all__'
    
    def get_image(self, obj):
        request = self.context.get('request')
        base_url = request.build_absolute_uri('/')
        image_path = obj.image.url.lstrip('/')
        return base_url + image_path


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ChangeEmailSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_email = serializers.EmailField(required=True)