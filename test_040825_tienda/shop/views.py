import json
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from shop_core.models import Articulo
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from shop_core.util.response import make_response, ResponseStatus
from django.db import transaction        
from shop_core.models import Stock, Movimiento, Venta
from app.jinja2 import calc_total


def get_carrito(request):
    if "carrito" not in request.session:
        request.session["carrito"] = {}

    return request.session.get("carrito", {})

def buy(request):
    carrito = get_carrito(request)
    articulos = Articulo.objects.filter(codigo__in=carrito.keys())
    usuario = request.user

    fondos = Movimiento.get_ingreso(usuario, False)
    total = calc_total(request)

    if fondos < total:
        messages.error(request, "No tienes fondos suficientes")
        return redirect("carrito")
    
    try:
        with transaction.atomic():
            for articulo in articulos:
                cantidad = carrito[articulo.codigo]

                monto = articulo.precio * cantidad
                
                if articulo.stock_total() < cantidad:
                    transaction.set_rollback(True)
                    messages.error(request, "No hay stock suficiente para el articulo " + articulo.nombre)
                    return redirect("carrito")

                stock = Stock.objects.create(
                    articulo=articulo,
                    cantidad=-cantidad,
                )

                movimiento = Movimiento.objects.create(
                    monto=-monto,
                    es_venta=True,
                    usuario=usuario
                )

                Venta.objects.create(
                    stock=stock,
                    movimiento=movimiento,
                    precio=articulo.precio,
                )
            
            if Movimiento.get_ingreso(usuario, False)<0:
                messages.error(request, "No tienes fondos suficientes")
                transaction.set_rollback(True)
                return redirect("carrito")

        request.session["carrito"] = {}
        request.session.modified = True

        messages.success(request, "Compra exitosa")
        return redirect("carrito")
    except Exception as e:
        messages.error(request, "Hubo un error en el servidor: " + str(e))
        return redirect("carrito")

    
def index(request):
    filtro = request.GET.get("filtro", "").strip()

    if filtro != "":
        articulos = Articulo.objects.filter(
             Q(nombre__icontains=filtro) | Q(codigo__icontains=filtro) | Q(descripcion__icontains=filtro)
         )
    else:
        articulos = Articulo.objects.all()

    return render(request, "shop_index.jinja", {
        "articulos": articulos, 
        "carrito": get_carrito(request),
        "filtro": filtro
    })

def detalles(request, codigo):
    articulo = Articulo.objects.filter(codigo=codigo).first()
    return render(request, "shop_detalles.jinja", {"articulo": articulo, "carrito": get_carrito(request)})

def carrito_post(request):
    try:
        data = json.loads(request.body)
    except Exception as e:
        return make_response(ResponseStatus.ERROR, "No se a enviado un JSON válido", status_code=500)

    codigo = data.get("codigo")
    cantidad = data.get("cantidad")

    if codigo is None or cantidad is None:
        return make_response(ResponseStatus.ERROR, "No se a enviado el codigo o la cantidad", status_code=500)
    
    try:
        cantidad = int(cantidad)
    except ValueError:
        return make_response(ResponseStatus.ERROR, "La cantidad debe ser un numero", status_code=500)

    if cantidad < 0:
        return make_response(ResponseStatus.ERROR, "La cantidad debe ser mayor a 0", status_code=500)
    
    if cantidad==0 and codigo in request.session["carrito"]:
        del request.session["carrito"][codigo]
        request.session.modified = True
        return make_response(ResponseStatus.SUCCESS, "Articulo eliminado del carrito", status_code=200)

    articulo = Articulo.objects.filter(codigo=codigo).first()

    if not articulo:
        return make_response(ResponseStatus.FAIL, "El articulo no existe", status_code=404)
    
    if cantidad > articulo.stock_total():
        cantidad = articulo.stock_total()

    request.session["carrito"][codigo] = cantidad
    request.session.modified = True

    return make_response(ResponseStatus.SUCCESS, "Articulo agregado al carrito", status_code=200)


def carrito_get(request):
    #Obtengo todos los articulos que estan en el carrito
    articulos = Articulo.objects.filter(codigo__in=get_carrito(request).keys())

    return render(request, "shop_cart.jinja", {"articulos": articulos, "carrito": get_carrito(request)})


@csrf_exempt
def carrito(request):
    if request.method != "POST":
        return carrito_get(request)
    
    return carrito_post(request)