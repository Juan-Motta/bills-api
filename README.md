# APLICACIÓN DE FACTURACIÓN
API Rest de facturacion que incluye manejo de clientes, productos y facturas contruido en Django

<hr>

### Requisitos Optimos
* Python 3.9.7

<hr>

### Configuracion
**1.** Creacion del entorno virtual
**2.** Instalacion de dependencias requeridas mediante el archivo requirements.txt
**3.** Creacion de migraciones
```
python manage.py makemigrations
```
```
python manage.py migrate
```
**4.** Creacion de superusuario para habilitacion del administrador
```
python manage.py createsuperuser
```
**5.** Inicializacion del servidor
```
python manage.py runserver
```
<hr>
### API

#### Token

###### POST - Obtencion de tokens
Devuelve un JSON con un token de acceso y un token de refresco, pide un correo y una contraseña valida en el body
URL:
```
http://localhost:8000/api/login/
```
Body:
```json
{
    "email": "usuario@example.com",
    "password": "12345"
}
```

###### POST - Refrescado de token de acceso
Devuelve un JSON con un token de acceso, pide un token de refresco en el body
URL:
```
http://localhost:8000/api/login/refresh/
```
Body:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
}
```
#### Clientes

###### GET - Obtener lista de clientes
Devuelve un JSON con una lista de clientes registrados en la base de datos, requiere token de autorizacion con permisos de administrador para acceder a la informacion
URL:
```
http://localhost:8000/api/clients/all
```

###### GET - Obtener cliente por id
Devuelve un JSON con los datos del cliente que correspondan al id, requiere un token de autorizacion generado por el mismo usuario a consultar o con permisos de administrador.
URL:
```
http://localhost:8000/api/clients/id/<id:int>
```

###### POST - Crear cliente
Crear un cliente con los datos proporcionados en el body
Crear
URL:
```
http://localhost:8000/api/clients/create/
```
Body:
```json
{
    "email": "cliente@example.com",
    "first_name": "Jhon",
    "last_name": "Doe",
    "document": "12345678",
    "password": "12345"
}
```

###### PUT - Actualizar cliente por id
Actualiza un cliente con los datos proporcionados en el body, requiere un token de autorizacion generado por el mismo usuario a actualizar o con permisos de administrador.
URL:
```
http://localhost:8000/api/clients/id/<id:int>
```
Body:
```json
{
    "first_name": "Jhon",
    "last_name": "Doe",
    "document": "12345678"
}
```

###### PUT - Actualizar contraseña de cliente por id
Actualiza la contraseña de un cliente con los datos proporcionados en el body, requiere un token de autorizacion generado por el mismo usuario a actualizar o con permisos de administrador.
URL:
```
http://localhost:8000/api/clients/password/<id:int>
```
Body:
```json
{
    "password": "12345"
}
```

###### DELETE - Eliminar cliente por id
Elimina el cliente con el id proporcionado, requiere un token de autorizacion generado por el mismo usuario a eliminar o con permisos de administrador.
URL:
```
http://localhost:8000/api/clients/id/<id:int>
```

#### Productos

###### GET - Obtener lista de productos
Devuelve un JSON con una lista de productos registrados en la base de datos
URL:
```
http://localhost:8000/api/products/all
```

###### GET - Obtener producto por id
Devuelve un JSON con los datos del producto que correspondan al id
URL:
```
http://localhost:8000/api/products/id/<id:int>
```

###### POST - Crear producto
Crear un cliente con los datos proporcionados en el body, requiere un token con permisos de administrador.
URL:
```
http://localhost:8000/api/products/create/
```
Body:
```json
{
    "name": "Producto 001",
    "description": "Descripcion del producto"
}
```

###### PUT - Actualizar producto por id
Actualiza un producto con los datos proporcionados en el body, requiere un token con permisos de administrador
URL:
```
http://localhost:8000/api/products/id/<id:int>
```
Body:
```json
{
    "name": "Producto 001",
    "description": "Descripcion del producto"
}
```

###### DELETE - Eliminar producto por id
Elimina el cliente con el id proporcionado, requiere un token con permisos de administrador.
URL:
```
http://localhost:8000/api/products/id/<id:int>
```

#### Facturas

###### GET - Obtener lista de facturas
Devuelve un JSON con una lista de facturas registrados en la base de datos, requiere un token con permisos de administrador
URL:
```
http://localhost:8000/api/bills/all
```

###### GET - Obtener factura por id
Devuelve un JSON con los datos de la factura que correspondan al id, requiere un token de autorizacion generado por el mismo usuario registrado en la factura o con permisos de administrador.
URL:
```
http://localhost:8000/api/bills/id/<id:int>
```

###### POST - Crear factura
Crear una factura con los datos proporcionados en el body, requiere un token de autenticación. Los valores para client y products corresponden a los IDs correspondientes de cada registro.
URL:
```
http://localhost:8000/api/bills/create/
```
Body:
```json
{
    "client": 1,
    "company_name": "My Company",
    "nit": "12345678",
    "code": "12345678",
    "products": [1,2]
}
```

###### PUT - Actualizar factura por id
Actualiza un producto con los datos proporcionados en el body, requiere un token con permisos de administrador
URL:
```
http://localhost:8000/api/bills/id/<id:int>
```
Body:
```json
{
    "client": 1,
    "company_name": "My Company",
    "nit": "12345678",
    "code": "12345678",
    "products": [1]
}
```

###### DELETE - Eliminar factura por id
Elimina el cliente con el id proporcionado, requiere un token con permisos de administrador.
URL:
```
http://localhost:8000/api/bills/id/<id:int>
```

#### CSV

###### Obtener CSV con datos de usuarios
Genera un archivo csv con la informacion de todos los clientes registrados
```
http://localhost:8000/api/clients/all/csv
```

###### Cargar CSV con datos de usuarios
Carga un archivo CSV y registra todos los usuarios contenidos en el mismo en la base de datos, requiere un token con permisos de administrador.

![image](https://user-images.githubusercontent.com/78517969/145653105-59159f3e-37e7-4583-9c22-d4efb6b476bd.png)


```
http://localhost:8000/api/clients/all/csv
```

Modelo del archivo CSV
```
id,email,first_name,last_name,document
1,admin@example.com,Jhon,Doe,12345678
```

#### PRUEBAS POSTMAN
```
https://www.getpostman.com/collections/53c7c562e3d462782a47
```
