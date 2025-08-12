from django.db import models
from django.core.validators import MinValueValidator
from .base_model import BaseModel
from shop_core.util.TTLCache import TTLCache
from django import forms

stock_cache = TTLCache(prefix="stock", ttl=10)

class Articulo(BaseModel):
    """
    Modelo que representa un artículo en el sistema.
    """
    id_articulo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, help_text="Nombre del artículo" )
    codigo = models.CharField(max_length=50, unique=True, help_text='Código único del artículo')
    descripcion = models.CharField(max_length=128, blank=True, null=True, help_text='Descripción del artículo')
    precio = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Precio del artículo'
    )

    imagen = models.ImageField(upload_to='articulos', null=True, blank=True)
    
    def stock_total(self, use_cache=True, clear_cache=False):
        def calc():
            return self.stocks.aggregate(
                total=models.Sum('cantidad')
            )['total'] or 0

        if clear_cache:
            stock_cache.remove(self.id_articulo)

        if use_cache:
            return stock_cache.get_or_default(self.id_articulo, calc)
        
        return calc()   
    stock_total.short_description = 'Stock Total'

    def save(self, *args, **kwargs):
        #Si el articulo aun no existe, no se crea un historial
        if self.id_articulo:
            #Importar aqui para evitar la importacion circular
            from .articulo_historial_model import ArticuloHistorial
            original = Articulo.objects.get(pk=self.pk)
            ArticuloHistorial.objects.create(
                articulo=self,
                nombre=original.nombre,
                codigo=original.codigo,
                descripcion=original.descripcion,
                precio=original.precio,
                imagen=original.imagen,
            )

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        ordering = ['nombre','codigo']

    def __str__(self):
        return f"{self.nombre} - {self.codigo}"

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = '__all__' 