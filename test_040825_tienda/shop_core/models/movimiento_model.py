from .base_model import BaseModel
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from shop_core.util.TTLCache import TTLCache

movimiento_cache = TTLCache(prefix="movimiento")

class Movimiento(BaseModel):
    id_movimiento = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    es_venta = models.BooleanField(default=False)
    es_transferencia = models.BooleanField(default=False)
    es_deposito = models.BooleanField(default=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movimientos')
    transferencia = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='movimientos_transferencia')

    def get_tipo_de_movimiento(self):
        if self.es_venta:
            return 'Venta'
        if self.es_transferencia:
            return 'Transferencia'
        if self.es_deposito:
            return 'Extraccion' if self.monto < 0 else 'Depósito'

    def clean(self):
        super().clean()
        campos_true = sum([
            self.es_venta,
            self.es_transferencia,
            self.es_deposito
        ])
        
        if campos_true > 1:
            raise ValidationError('Solo uno de los tipos puede ser True a la vez')

    @staticmethod
    def get_ingreso(usuario, use_cache=True):
        if use_cache:
            return movimiento_cache.get_or_default(usuario.id, lambda: usuario.movimientos.aggregate(
                total=models.Sum('monto')
            )['total'] or 0)
        
        movimiento_cache.remove(usuario.id)

        return Movimiento.objects.filter(usuario=usuario).aggregate(
            total=models.Sum('monto')
        )['total'] or 0