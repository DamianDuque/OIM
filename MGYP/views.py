from django.shortcuts import render
from MGYP.models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.


def login1(request):
    if request.user.is_authenticated:
        return redirect('../home/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('../home/')
            else:

                messages.info(request, 'Nombre de usuario o contraseña')
                messages.info(request, 'están incorrectos')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('../login/')


@login_required(login_url='../login/')
def home(request):
    usuarios_obj = Empleado.objects.get(nombre=request.user)
    return render(request, 'home.html', {'nombre': usuarios_obj.nombre})

@login_required(login_url='../login/')
def inventario(request):
    usuarios_obj = Empleado.objects.get(nombre=request.user)
    return render(request, 'inventario.html', {'nombre': usuarios_obj.nombre})