from django.templatetags.static import static
from django.urls import reverse
from jinja2 import Environment
from django.middleware.csrf import get_token
from shop_core.models.articulo_model import Articulo
from shop_core.models.movimiento_model import Movimiento
from datetime import datetime
from shop_core.util.TTLCache import TTLCache

carrito_total = TTLCache(prefix="carrito_total")

def get_monto(user):
    return Movimiento.get_ingreso(user)

def format_datetime(value, format='%d/%m/%Y %H:%M'):
    if value is None:
        return ''
    return value.strftime(format)

def calc_total(request):
    def calc():
        carrito = request.session.get("carrito", {})
        articulos = Articulo.objects.filter(codigo__in=carrito.keys())

        total = 0
        for articulo in articulos:
            total += articulo.precio * carrito[articulo.codigo]
        
        return total
    
    return carrito_total.get_or_default(request.user.id, calc)

def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
        'csrf_token': get_token,
        'get_monto': get_monto,
        'carrito_calc_total': calc_total,
    })
    env.filters['datetime'] = format_datetime
    return env
