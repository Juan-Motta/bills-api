from django.urls import path

from .views import (
    client_all_api_view,
    client_create_api_view,
    client_by_id_api_view,
    client_update_password_api_view,
    export_csv_api_view,
    import_csv_api_view
)

urlpatterns = [
    path(
        'all/',
        client_all_api_view,
        name='client_list_all'
    ),
    path(
        'create/',
        client_create_api_view,
        name='client_create'
    ),
    path(
        'id/<int:id>',
        client_by_id_api_view,
        name='client_by_id'
    ),
    path(
        'password/<int:id>',
        client_update_password_api_view,
        name='client_password_update'
    ),
    path(
        'all/csv',
        export_csv_api_view,
        name='client_list_all_csv'
    ),
    path(
        'create/csv',
        import_csv_api_view,
        name='client_create_csv'
    ),
]
