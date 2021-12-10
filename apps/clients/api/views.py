import csv
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend

from apps.clients.models import Client
from apps.clients.api.serilizers import (
    ClientListSerializer,
    ClientCreateSerializer,
    ClientUpdateSerializer,
    ClientUpdatePasswordSerializer
)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def client_all_api_view(request):
    """
    Obtains all clients, only for admin users credentials
    """
    if request.method == 'GET':
        # queryset
        client = Client.objects.all()
        clients_serializer = ClientListSerializer(client, many=True)
        return Response(clients_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def client_create_api_view(request):
    """"
    Creates a client
    """
    if request.method == 'POST':
        # create
        client_serializer = ClientCreateSerializer(data=request.data)
        if client_serializer.is_valid():
            client_serializer.save()
            return Response({'message': 'Cliente creado correctamente', 'data': client_serializer.data}, status=status.HTTP_201_CREATED)
        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def client_by_id_api_view(request, id=None):
    """
    Lists, Updates and Deletes a client by id, only accessable by either an user itself or an admin user
    """
    # get id from jwt obtained from headers
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
    client_id = valid_data['user_id']
    # query permissions calling the user instance using id from token
    client_is_staff = Client.objects.filter(id=client_id).first().is_staff
    # if user obtained is admin, it can acces to any client data, else it only can access to its own info
    if client_is_staff or client_id == id:
        client = Client.objects.filter(id=id).first()
    else:
        return Response({'errors': 'No tiene los permisos necesarios para realizar esta operación'}, status=status.HTTP_401_UNAUTHORIZED)

    # validation
    if client:
        # retrieve
        if request.method == 'GET':
            client_serializer = ClientListSerializer(client)
            return Response(client_serializer.data, status=status.HTTP_200_OK)

        # update
        elif request.method == 'PUT':
            client_serializer = ClientUpdateSerializer(
                client, data=request.data)
            if client_serializer.is_valid():
                client_serializer.save()
                return Response({'message': 'Cliente actualizado correctamente', 'data': client_serializer.data}, status=status.HTTP_200_OK)
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # delete
        elif request.method == 'DELETE':
            client.delete()
            return Response({'message': 'Cliente Eliminado correctamente!'}, status=status.HTTP_200_OK)

    return Response({'errors': 'No se ha encontrado un cliente con estos datos'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, ])
def client_update_password_api_view(request, id=None):
    """
    Updates a specific client password, only accessable by either an user itself or an admin user
    """
    # get id from jwt obtained from headers
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
    client_id = valid_data['user_id']
    # query permissions from user id obtained from token
    client_is_staff = Client.objects.filter(id=client_id).first().is_staff

    # if user obtained from token is admin, it can acces to any user data, else only can access to its own info
    if client_is_staff or client_id == id:
        client = Client.objects.filter(id=id).first()
    else:
        return Response({'errors': 'No tiene los permisos necesarios'}, status=status.HTTP_401_UNAUTHORIZED)

    if client:
        # update
        if request.method == 'PUT':
            client_serializer = ClientUpdatePasswordSerializer(
                client, data=request.data)
            if client_serializer.is_valid():
                client_serializer.save()
                return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def export_csv_api_view(request):
    """
    Generates a csv file with all clients info inside
    """
    if request.method == 'GET':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.DictWriter(response, fieldnames=[
                                'id', 'email', 'first_name', 'last_name', 'document'])
        writer.writeheader()
        for client in Client.objects.all():
            writer.writerow({
                'id': client.id,
                'email': client.email,
                'first_name': client.first_name,
                'last_name': client.last_name,
                'document': client.document
            })
        return response


@api_view(['POST'])
@permission_classes((IsAdminUser, ))
def import_csv_api_view(request):
    """
    Generates clients based on csv file
    """
    if request.method == 'POST':
        # creates a file storage and initializes required variables
        fs = FileSystemStorage(location='temp/')
        client_list = []
        # gets content from request and reads it
        file = request.FILES['file']
        content = file.read()
        file_content = ContentFile(content)
        # creates a file based on the data gotten from request and save it on server
        file_name = fs.save(
            "_temp.csv",
            file_content
        )
        tmp_file = fs.path(file_name)
        # reads the saved file and creates a client instance based on the info stored inside it.
        csv_file = open(tmp_file, errors='ignore')
        reader = csv.reader(csv_file)
        next(reader)
        for index, row in enumerate(reader):
            (
                _,
                email,
                first_name,
                last_name,
                document
            ) = row
            client_list.append(
                Client(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    document=document
                )
            )
        # saves all instances on the db
        Client.objects.bulk_create(client_list)
        return Response({'message': 'Clientes creados correctaente'}, status=status.HTTP_201_CREATED)
