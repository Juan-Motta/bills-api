from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/', include('apps.clients.api.urls')),
    path('api/products/', include('apps.products.api.urls')),
    path('api/bills/', include('apps.bills.api.urls')),
    path('api/login/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
