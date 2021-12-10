from rest_framework import serializers

from apps.clients.api.serilizers import ClientListSerializer
from apps.bills.models import Bill


class BillListSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for GET methods.
    """
    client = ClientListSerializer()

    class Meta:
        model = Bill
        fields = [
            'id',
            'client',
            'company_name',
            'nit',
            'code',
            'products'
        ]
        depth = 1


class BillSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting models instances into JSON files and viceversa used for POST and PUT methods.
    """
    class Meta:
        model = Bill
        fields = [
            'id',
            'client',
            'company_name',
            'nit',
            'code',
            'products'
        ]
        extra_kwargs = {'products': {'required': True}}
