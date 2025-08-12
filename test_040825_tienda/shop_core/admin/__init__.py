from django.utils import timezone
from django.contrib import admin
from shop_core.models import Articulo, ArticuloHistorial, Stock, Movimiento, Venta
from .admin_base import BaseAdmin

# Verificar si la acción existe antes de intentar deshabilitarla
if 'delete_selected' in admin.site._actions:
    admin.site.disable_action('delete_selected')

@admin.register(Articulo)
class ArticuloAdmin(BaseAdmin):
    list_display = ('nombre', 'codigo', 'precio', 'stock_total')
    search_fields = ('nombre', 'codigo')
    readonly_fields = BaseAdmin.readonly_fields + ('stock_total',)

@admin.register(ArticuloHistorial)
class ArticuloHistorialAdmin(BaseAdmin):
    list_display = ('nombre', 'codigo', 'precio', 'get_created_at')
    search_fields = ('nombre', 'codigo')

    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Fecha de edicion'  # Nombre personalizado
    get_created_at.admin_order_field = 'created_at'

@admin.register(Stock)
class StockAdmin(BaseAdmin):
    list_display = ('articulo', 'cantidad')
    list_filter = BaseAdmin.list_filter +  ('articulo',)
    
    
@admin.register(Movimiento)
class MovimientoAdmin(BaseAdmin):
    list_display = ('get_usuario', 'monto', 'get_tipo')

    def get_usuario(self, obj):
        return obj.usuario
    get_usuario.short_description = 'Usuario'

    def get_tipo(self, obj):
        if obj.es_venta:
            return 'Venta'
        if obj.es_transferencia:
            return 'Transferencia'
        if obj.es_deposito:
            return 'Extraccion' if obj.monto < 0 else 'Depósito'
    get_tipo.short_description = 'Tipo'
    

@admin.register(Venta)
class VentaAdmin(BaseAdmin):
    list_display = ('stock', 'precio',)
