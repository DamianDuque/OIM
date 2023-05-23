from django.shortcuts import render
from MGYP.models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.

def registro(request):
    if request.user.is_authenticated:
        return redirect('../home/')
    else:
        class CreateUserForm(UserCreationForm):
            class Meta:
                model = User
                fields = ['username', 'password1', 'password2']
        form = CreateUserForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                pwd = form.cleaned_data.get('password1')
                messages.success(request, 'La cuenta fue creada')
                messages.success(request, 'satisfactoriamente para ' + user)
                usuarioN = Empleado(nombre=user, rol="administrador")
                usuarioN.save()
                user2 = authenticate(request, username=user, password=pwd)
                login(request, user2)
                return redirect('../home/')
                
        context = {'form': form}
        return render(request, 'registro.html', context)

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

@login_required(login_url='../login/')
def productos(request):
    producto_obj = Producto.objects.all()
    return render(request, 'productos.html', {'producto': producto_obj})

@login_required(login_url='../login/')
def nuevo_producto(request):
    usuarios_obj = Empleado.objects.get(nombre=request.user)
    try:
        nombre = request.POST['nombre']
        codigo_barras = request.POST['codigo_barras']
        descripcion = request.POST['descripcion']
        peso = request.POST['peso']
    except:
        mensaje = ''
        return render(request, 'nuevo_producto.html', {'mensaje': mensaje})
    else:
        mensaje = "Se ha creado un nuevo producto con éxito"
        db_producto = Producto(codigo_de_barras=codigo_barras, nombre=nombre, descripcion=descripcion, peso=peso)
        db_producto.save()
        db_actividad = Actividad(id_empleado_id=usuarios_obj.id_empleado, tipo_actividad='nuevo producto')
        db_actividad.save()
    return render(request, 'nuevo_producto.html', {'mensaje': mensaje})

@login_required(login_url='../login/')
def actividad(request):
    actividad_obj = Actividad.objects.all()
    return render(request, 'actividad.html', {'actividad': actividad_obj})