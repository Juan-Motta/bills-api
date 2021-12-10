from django.urls import path

from .views import (
    product_all_api_view,
    product_create_api_view,
    product_api_view
)


urlpatterns = [
    path(
        'all',
        product_all_api_view,
        name='all_products'
    ),
    path(
        'id/<int:id>',
        product_api_view,
        name='detailed_product'
    ),
    path(
        'create/',
        product_create_api_view,
        name='create_product'
    )
]
