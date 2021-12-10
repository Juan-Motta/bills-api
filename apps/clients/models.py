
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class ClientManager(BaseUserManager):
    """
    Custom client model manager.
    """

    def _create_user(self, email, first_name, last_name, document, password, is_staff, is_superuser, **extra_fields):
        """
        Create and save a User with the given data.
        """
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            document=document,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, first_name, last_name, document, password=None, **extra_fields):
        """
        Call _create_user function setting the respective parameters for a user.
        """
        return self._create_user(email, first_name, last_name, document, password, False, False, **extra_fields)

    def create_superuser(self, email, first_name, last_name, document, password=None, **extra_fields):
        """
        Call _create_user function setting the respective parameters for a superuser.
        """
        return self._create_user(email, first_name, last_name, document, password, True, True, **extra_fields)


class Client(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'Correo Electrónico',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(
        'Nombres',
        max_length=255,
    )
    last_name = models.CharField(
        'Apellidos',
        max_length=255,
    )
    document = models.CharField(
        'Documento',
        max_length=20,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = ClientManager()

    class Meta:
        """Metadata definition for client model"""
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'document',
    ]

    def __str__(self):
        """Unicode representation for client"""
        return f'{self.id} {self.first_name} {self.last_name}'
