from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from shop_core.models import Articulo, Stock, Venta, ArticuloHistorial, ArticuloForm

# Create your views here.
@staff_member_required
def index(request):
    return render(request, "admin_index.jinja")

@staff_member_required
def articulos(request):
    articulos = Articulo.objects.all()
    return render(request, "admin_articulos.jinja", {"articulos": articulos})

@staff_member_required
def ventas(request):
    ventas = Venta.objects.all()
    return render(request, "admin_ventas.jinja", {"ventas": ventas})

@staff_member_required
@require_POST
def stock(request):
    codigo = request.POST.get("codigo", "").strip()
    cantidad = request.POST.get("cantidad", "").strip()

    if request.POST.get("to_detalles", "").strip() == "1":
        to_page = redirect("admin_detalles", codigo=codigo)
    else:
        to_page = redirect("admin_articulos")

    if codigo == "" or cantidad == "":
        messages.error(request, "No se a enviado el codigo o la cantidad")
        return to_page
    
    try:
        cantidad = int(cantidad)
    except ValueError:
        messages.error(request, "La cantidad debe ser un numero")
        return to_page
    
    if cantidad == 0:
        messages.error(request, "La cantidad debe ser mayor a 0")
        return to_page

    articulo = Articulo.objects.filter(codigo=codigo).first()
    if not articulo:
        messages.error(request, "El articulo no existe")
        return to_page


    total = articulo.stock_total(use_cache=False, clear_cache=True)
    if cantidad < 0:
         
        if (total + cantidad) < 0:
            messages.error(request, "No hay stock suficiente")
            return to_page

    Stock.objects.create(
        articulo=articulo,
        cantidad=cantidad,
    )
    
    messages.success(request, "Stock actualizado exitosamente")
    return to_page

@staff_member_required
@require_POST
def eliminar(request):
    codigo = request.POST.get("codigo", "").strip()

    if codigo == "":
        messages.error(request, "No se a enviado el codigo")
        return redirect("admin_articulos")

    articulo = Articulo.objects.filter(codigo=codigo).first()
    if not articulo:
        messages.error(request, f"El articulo {codigo} no existe")
        return redirect("admin_articulos")
    
    articulo.delete()
    messages.success(request, "Articulo eliminado exitosamente")
    return redirect("admin_articulos")

@staff_member_required
def detalles(request, codigo):
    articulo = Articulo.objects.filter(codigo=codigo).first()
    if not articulo:
        messages.error(request, f"El articulo no existe")
        return redirect("admin_articulos")

    ventas = Venta.objects.filter(stock__articulo=articulo).all()


    return render(request, "admin_detalles.jinja", {
        "articulo": articulo,
        "stocks": articulo.stocks.all(),
        "ventas": ventas,
        "historial": articulo.historial.all(),
    })

@staff_member_required
@require_POST
def restaurar(request):
    historial_id = request.POST.get("historial_id", "").strip()

    if historial_id == "":
        messages.error(request, "No se a enviado el id del historial")
        return redirect("admin_articulos")
    
    articulo_historial = ArticuloHistorial.objects.filter(id_articulo_historial=historial_id).first()
    if not articulo_historial:
        messages.error(request, "El historial no existe")
        return redirect("admin_articulos")
    
    articulo = articulo_historial.articulo
    
    articulo.nombre = articulo_historial.nombre
    articulo.codigo = articulo_historial.codigo
    articulo.descripcion = articulo_historial.descripcion
    articulo.precio = articulo_historial.precio
    articulo.imagen = articulo_historial.imagen
    
    articulo.save()
    
    messages.success(request, "Articulo restaurado exitosamente")
    return redirect("admin_detalles", codigo=articulo.codigo)

@staff_member_required
@require_POST
def cambiar_image(request):
    codigo = request.POST.get("codigo", "").strip()
    
    if codigo == "":
        messages.error(request, "No se a enviado el codigo")
        return redirect("admin_articulos")
    
    articulo = Articulo.objects.filter(codigo=codigo).first()
    if not articulo:
        messages.error(request, "El articulo no existe")
        return redirect("admin_articulos")
    
    imagen = request.FILES.get("imagen")
    if not imagen:
        messages.error(request, "No se a enviado la imagen")
        return redirect("admin_articulos")
    
    articulo.imagen = imagen
    articulo.save()
    
    messages.success(request, "Imagen cambiada exitosamente")
    return redirect("admin_detalles", codigo=articulo.codigo)

@staff_member_required
@require_POST
def modificar(request):
    form = ArticuloForm(request.POST, request.FILES)
    if form.is_valid(): 
        articulo = form.save()
        messages.success(request, "Articulo modificado exitosamente")
        return redirect("admin_detalles", codigo=articulo.codigo)

    #Muestra los errores en los datos enviados
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, f"Error en {field}: {error}")
    return redirect("admin_index")