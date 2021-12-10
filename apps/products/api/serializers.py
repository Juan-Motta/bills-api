from rest_framework import serializers

from apps.products.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for GET methods.
    """
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description'
        ]


class ProductSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for POST and PUT methods.
    """
    class Meta:
        model = Product
        fields = [
            'name',
            'description'
        ]
