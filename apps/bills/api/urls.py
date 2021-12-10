from django.urls import path

from .views import (
    bill_all_api_view,
    bill_create_api_view,
    bill_api_view
)


urlpatterns = [
    path(
        'all',
        bill_all_api_view,
        name='all_bills'
    ),
    path(
        'create/',
        bill_create_api_view,
        name='create_bill'
    ),
    path(
        'id/<int:id>',
        bill_api_view,
        name='detailed_bill'
    )
]
