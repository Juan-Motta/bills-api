from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import (
    IsAdminUser,
    AllowAny
)
from rest_framework.response import Response

from apps.products.api.permissions import IsAdminUserCustom
from apps.products.api.serializers import (
    ProductSerializer,
    ProductListSerializer
)
from apps.products.models import Product


@api_view(['GET'])
@permission_classes((AllowAny, ))
def product_all_api_view(request):
    """
    Obtains all products
    """
    if request.method == 'GET':
        # queryset
        product = Product.objects.all()
        products_serializer = ProductListSerializer(product, many=True)
        return Response(products_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAdminUser, ))
def product_create_api_view(request):
    """"
    Creates a product, only for admin users credentials
    """
    if request.method == 'POST':
        # create
        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({'message': 'Producto creado correctamente', 'data': product_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAdminUserCustom, ))
def product_api_view(request, id=None):
    """
    Lists, Updates and Deletes a client by id, only accessable by an admin user if methos are put and delete
    """
    # queryset
    product = Product.objects.filter(id=id).first()

    if product:
        # retrieve
        if request.method == 'GET':
            product_serializer = ProductListSerializer(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        # update
        elif request.method == 'PUT':
            product_serializer = ProductSerializer(product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response({'message': 'Producto actualizado correctamente', 'data': product_serializer.data}, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # delete
        elif request.method == 'DELETE':
            product.delete()
            return Response({'message': 'Producto eliminado correctamente'}, status=status.HTTP_200_OK)

    return Response({'errors': 'No se ha encontrado un producto con los datos proporcionados'}, status=status.HTTP_400_BAD_REQUEST)
