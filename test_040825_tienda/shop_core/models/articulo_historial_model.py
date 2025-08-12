from django.db import models
from django.core.validators import MinValueValidator
from .base_model import BaseModel
from .articulo_model import Articulo

class ArticuloHistorial(BaseModel):
    id_articulo_historial = models.AutoField(primary_key=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name="historial")
    nombre = models.CharField(max_length=50, help_text="Nombre del artículo" )
    codigo = models.CharField(max_length=50, help_text='Código único del artículo')
    descripcion = models.CharField(max_length=128, blank=True, null=True, help_text='Descripción del artículo')
    precio = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Precio del artículo'
    )

    imagen = models.ImageField(upload_to='articulos', null=True, blank=True)