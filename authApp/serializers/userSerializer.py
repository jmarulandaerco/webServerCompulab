from rest_framework import serializers
from authApp.models.user import User

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        return User.objects.create(**validated_data)
