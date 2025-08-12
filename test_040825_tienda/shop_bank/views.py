from email import message
from django.shortcuts import render, redirect
from shop_core.models import Movimiento
from django.contrib import messages
from django.contrib.auth.models import User

def transferir(request):
    if request.method == "POST":
        monto = request.POST.get("monto", 0)
        usuario = request.POST.get("usuario", "").strip()

        if len(usuario) == 0:
            messages.error(request, "No se a enviado el usuario")
            return redirect('fondos')

        try:
            monto = float(monto)
        except ValueError:
            messages.error(request, "El monto debe ser un numero")
            return redirect('fondos')

        if monto < 0:
            messages.error(request, "El monto debe ser mayor a 0")
            return redirect('fondos')

        fondos = float(Movimiento.get_ingreso(request.user, False))
        if (fondos - monto) < 0:
            messages.error(request, "No tienes fondos suficientes")
            return redirect('fondos')

        usuario = User.objects.filter(username=usuario).first()
        if not usuario:
            messages.error(request, "El usuario no existe")
            return redirect('fondos')

        Movimiento.objects.create(
            monto=-monto,
            es_transferencia=True,
            usuario=request.user,
            transferencia=usuario
        )

        Movimiento.objects.create(
            monto=monto,
            es_transferencia=True,
            usuario=usuario,
            transferencia=request.user
        )

        messages.success(request, f"Fondos transferidos exitosamente")

        return redirect('fondos')

# Create your views here.
def index(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        monto = request.POST.get("monto", 0)

        try:
            monto = float(monto)
        except ValueError:
            messages.error(request, "El monto debe ser un numero")
            return redirect('fondos')

        if monto == 0:
            messages.error(request, "No se a enviado el monto")
            return redirect('fondos')

        if monto < 0:
            fondos = float(Movimiento.get_ingreso(user, False))
            if (fondos + monto) < 0:
                messages.error(request, "No tienes fondos suficientes")
                return redirect('fondos')
            

        Movimiento.objects.create(
            monto=monto,
            es_deposito=True,
            usuario=user
        )

        messages.success(request, f"Fondos {'ingresados' if monto>0 else 'extraidos' } exitosamente")

        return redirect('fondos')

    movimientos = Movimiento.objects.filter(usuario=user)
    total = Movimiento.get_ingreso(user)

    return render(request, "bank_index.jinja", {"movimientos": movimientos, "total": total})