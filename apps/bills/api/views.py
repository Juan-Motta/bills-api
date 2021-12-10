from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend

from .permissions import IsAdminUserCustom
from apps.bills.models import Bill
from apps.clients.models import Client
from apps.bills.api.serializers import (
    BillSerializer,
    BillListSerializer
)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def bill_all_api_view(request):
    """
    Obtains all bills
    """
    if request.method == 'GET':
        # queryset
        bills = Bill.objects.all()
        bills_serializer = BillListSerializer(bills, many=True)
        return Response(bills_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def bill_create_api_view(request):
    """"
    Creates a bill, only for admin users credentials
    """
    if request.method == 'POST':
        # create
        bill_serializer = BillSerializer(data=request.data)
        if bill_serializer.is_valid():
            bill_serializer.save()
            return Response({'message': 'Factura creada correctamente', 'data': bill_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(bill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAdminUserCustom, ))
def bill_api_view(request, id=None):
    """
    Lists, Updates and Deletes a bill by id, only accessable by the user itself to its own bill or by an admin
    """
    # get id from jwt obtained from headers
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
    user_id = valid_data['user_id']
    # query permissions calling the user instance using id from token
    client_is_staff = Client.objects.filter(id=user_id).first().is_staff
    # query bill by id
    bill = Bill.objects.filter(id=id).first()
    # if user obtained from token is admin, it can acces to any user data, else only can access to its own info
    if not client_is_staff and not user_id == bill.client.id:
        return Response({'message': 'No tiene los permisos necesarios para realizar esta operación'}, status=status.HTTP_401_UNAUTHORIZED)
    # validation
    if bill:
        # retrieve
        if request.method == 'GET':
            bill_serializer = BillListSerializer(bill)
            return Response(bill_serializer.data, status=status.HTTP_200_OK)
        # update
        elif request.method == 'PUT':
            bill_serializer = BillSerializer(bill, data=request.data)
            if bill_serializer.is_valid():
                bill_serializer.save()
                return Response({'message': 'Factura actualizado correctamente', 'data': bill_serializer.data}, status=status.HTTP_200_OK)
            return Response(bill_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # delete
        elif request.method == 'DELETE':
            bill.delete()
            return Response({'message': 'Factura eliminado correctamente'}, status=status.HTTP_200_OK)

    return Response({'errors': 'No se ha encontrado una factura con los datos proporcionados'}, status=status.HTTP_400_BAD_REQUEST)
