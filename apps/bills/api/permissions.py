from rest_framework.permissions import IsAdminUser


class IsAdminUserCustom(IsAdminUser):
    """
    Allow acces to any user to GET methods but require admin credentials for POST, PUT and DELETE methods
    """

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return super().has_permission(request, view)
