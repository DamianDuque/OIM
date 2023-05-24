from django.shortcuts import render
from MGYP.models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from collections import Counter
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
def historial(request):
    actividad_obj = Actividad.objects.all().order_by('-fecha_actividad')
    return render(request, 'historial.html', {'actividad': actividad_obj})

@login_required(login_url='../login/')
def ingreso_productos(request):
    usuarios_obj = Empleado.objects.get(nombre=request.user)
    try:
        id_bodega = request.POST['id_bodega']
        productos = request.POST['productos']
        id_compra = request.POST['id_compra']
    except:
        compras_obj = Compras.objects.filter(estado_compra='por recibir')
        return render(request, 'ingreso_productos.html', {'compras': compras_obj, 'mensaje': ''})
    else:

        #Elementos que vienen de la base de datos
        compra_objeto = Compras.objects.get(id_compra=id_compra)
        str_pr_compra = compra_objeto.lista_productos
        lista_pr_compra = str_pr_compra.split()

        # -- Arreglos de productos y cantidades -- #
        lista_productos_compra = list(Counter(lista_pr_compra).keys())
        cantidades_productos_compra = list(Counter(lista_pr_compra).values())
        # -- Organizar lista recibida de compras -- #
        lista_organizada_compra = list(sorted(zip(lista_productos_compra,cantidades_productos_compra)))

        #Elementos que salen del formulario
        lista_productos_temp = productos.splitlines()
        print(lista_productos_temp)
        
        # -- Areglos de productos y cantidades -- #
        lista_productos = list(Counter(lista_productos_temp).keys())
        cantidades = list(Counter(lista_productos_temp).values())

        # -- Organizar lista scaneada para ingresar -- #
        lista_organizada_ingreso = list(sorted(zip(lista_productos,cantidades)))

        # -- Revision listas para marcar el estado del ingreso -- #

        ## --- Opcion 2, Revision paso a paso --- ##
        if len(lista_organizada_compra) != len(lista_organizada_ingreso):
            if len(lista_organizada_compra) > len(lista_organizada_ingreso):
                estado_recepcion = "pendiente por revision"
                notas_recepcion = "Notas: Faltan productos por recibir."
                # Se pueden almancenar en variable para luego notificar al usuario
            elif len(lista_organizada_compra) < len(lista_organizada_ingreso):
                estado_recepcion = "pendiente por revision"
                print("Notas: Se recibieron productos de más.")
                # Se pueden almacenar en variable para luego notificar al usuario
        else:
            if lista_organizada_compra == lista_organizada_ingreso:
                estado_recepcion = "OK"
                notas_recepcion = "Notas: Todo en orden. Productos y cantidades coinciden."
            '''for z in range (len(lista_organizada_compra)):
                if lista_organizada_compra[z] == lista_organizada_ingreso[z]:
                    print("Posicion " + str(z) + "en orden")
                    # Se pueden almancenar en variable para luego notificar al usuario
                else:
                    print("pendiente revision en" + str(z))
                    # Se pueden almancenar en variable para luego notificar al usuario'''
        


        mensaje = "Se ha creado un nuevo producto con éxito"
        db_recepcion = Recepcion(id_compra_id=id_compra, id_bodega_id=id_bodega, id_empleado_id=usuarios_obj.id_empleado, lista_productos=lista_productos, cantidades_productos=cantidades, estado_recepcion=estado_recepcion, notas_recepcion=notas_recepcion)
        db_recepcion.save()
        
        db_inventario = Inventario(id_recepcion_id = db_recepcion.id_recepcion, id_bodega_id=id_bodega,lista_productos=lista_productos, cantidades_productos=cantidades)
        db_inventario.save()
        compras_obj = Compras.objects.filter(estado_compra='por recibir')
        return render(request, 'ingreso_productos.html', {'compras': compras_obj, 'mensaje': mensaje})

@login_required(login_url='../login/')
def ingreso_productos_next(request):
    try:
        id_compra = request.POST['id_compra']
    except:
        compras_obj = Compras.objects.filter(estado_compra='por recibir')
        return render(request, 'ingreso_productos.html', {'compras': compras_obj})
    else:
        bodegas_obj = Bodega.objects.all()
        compras_obj = Compras.objects.get(id_compra=id_compra)
        return render(request, 'ingreso_productos_next.html', {'compras': compras_obj, 'bodegas': bodegas_obj, 'id_compra':id_compra})