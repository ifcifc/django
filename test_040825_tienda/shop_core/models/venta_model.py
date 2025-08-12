from django.db import models
from .base_model import BaseModel
from .stock_model import Stock
from django.core.validators import MinValueValidator
from .movimiento_model import Movimiento

class Venta(BaseModel):
    id_venta = models.AutoField(primary_key=True)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='ventas')
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE, related_name='ventas')
    precio = models.DecimalField(max_digits=15, decimal_places=2, help_text="Precio de venta", validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Venta precio: {self.precio}"