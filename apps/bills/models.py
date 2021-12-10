from django.db import models

from apps.clients.models import Client
from apps.products.models import Product


class Bill(models.Model):
    """Model representation for bills"""
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Cliente'
    )
    company_name = models.CharField(
        'Nombre Compañia',
        max_length=255,
    )
    nit = models.CharField(
        'NIT',
        max_length=30,
    )
    code = models.CharField(
        'Codigo',
        max_length=30,
    )
    products = models.ManyToManyField(
        Product
    )

    class Meta:
        """Metadata definition for bill model"""
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['company_name', 'nit']

    def __str__(self):
        """Unicode representation for bills"""
        return f'{self.id} - {self.company_name} - {self.nit} - {self.client}'
