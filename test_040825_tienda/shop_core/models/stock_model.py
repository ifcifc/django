from django.db import models
from .base_model import BaseModel
from .articulo_model import Articulo

class Stock(BaseModel):
    id_stock = models.AutoField(primary_key=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name='stocks')
    cantidad = models.IntegerField(default=0, help_text="Cantidad de stock")
    
    def __str__(self):
        return f"{self.articulo} - Cantidad: {self.cantidad}"