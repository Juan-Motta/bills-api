from django.db import models


class Product(models.Model):
    """Model representation for Products"""
    name = models.CharField(
        'Nombre',
        max_length=50,
    )
    description = models.CharField(
        'Descripcion',
        max_length=255,
    )

    class Meta:
        """Metadata definition for product model"""
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name', 'description']

    def __str__(self):
        """Unicode representation for product"""
        return f'{self.id} - {self.name}'
