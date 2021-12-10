from rest_framework import serializers

from apps.clients.models import Client


class ClientListSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for GET methods.
    """
    class Meta:
        model = Client
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'document',
            'is_active',
            'is_staff',
        ]


class ClientCreateSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for POST method.
    """
    class Meta:
        model = Client
        fields = [
            'email',
            'first_name',
            'last_name',
            'document',
            'password',
        ]

    # Hash the password when the register is created
    def create(self, validated_data):
        client = Client(**validated_data)
        client.set_password(validated_data['password'])
        client.save()
        return client


class ClientUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for PUT method.
    """
    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'document',
        ]


class ClientUpdatePasswordSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for PUT method.
    """
    class Meta:
        model = Client
        fields = [
            'password',
        ]

    # Hash the password when the register is updated
    def update(self, instance, validated_data):
        updated_client = super().update(instance, validated_data)
        updated_client.set_password(validated_data['password'])
        updated_client.save()
        return updated_client
