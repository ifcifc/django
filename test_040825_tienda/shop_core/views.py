from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

# Create your views here.

def index(request):
    return render(request, "index.jinja", {"title": "Inicio"})

def user_logout(request):
    logout(request)
    return redirect('index')

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login exitoso, Bienvenido!')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    
    return render(request, 'login.jinja')

@csrf_protect
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, "signup.jinja", {"title": "Registro - Error"})
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe')
            return render(request, "signup.jinja", {"title": "Registro - Error"})
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, "signup.jinja", {"title": "Registro - Error"})
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        login(request, user)
        messages.success(request, 'Cuenta creada exitosamente')
        return redirect('index')
    
    return render(request, "signup.jinja", {"title": "Registro"})
