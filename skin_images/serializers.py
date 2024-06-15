from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    def is_valid(self):
        return super().is_valid(raise_exception=True)
    
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass