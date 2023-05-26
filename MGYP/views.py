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
    return render(request, 'home.html', {'nombre': usuarios_obj.nombre, 'rol': usuarios_obj.rol})

@login_required(login_url='../login/')
def inventario(request):
    usuarios_obj = Empleado.objects.get(nombre=request.user)
    bodegas_obj = Bodega.objects.all()
    return render(request, 'inventario.html', {'nombre': usuarios_obj.nombre, 'bodegas':bodegas_obj})

@login_required(login_url='../login/')
def inventario_next(request):
    id_bodega = request.POST['id_bodega']
    inventario_obj = Inventario.objects.get(id_bodega=id_bodega)
    str_pr_inventario = inventario_obj.lista_productos
    lista_pr_inventario = str_pr_inventario.split()

    # -- Arreglos de productos y cantidades -- #
    lista_productos_inventario = list(Counter(lista_pr_inventario).keys())
    cantidades_productos_inventario = list(Counter(lista_pr_inventario).values())
    # -- Organizar lista recibida de compras -- #
    lista_organizada_inventario = list(sorted(zip(lista_productos_inventario,cantidades_productos_inventario)))
    list_productos = Producto.objects.all()
    return render(request, 'inventario_next.html', {'id_bodega':id_bodega, 'list_productos':list_productos})

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
        
        inventario_obj = Inventario.objects.all()
        if len(inventario_obj) != 0:
            
            for inventario in inventario_obj:
                inventario.lista_productos = inventario.lista_productos+" "+codigo_barras
                inventario.save() ## update lista_productos
        else:
            
            bodega_obj = Bodega.objects.all()
            
            for bodega in bodega_obj:
                db_inventario = Inventario(id_bodega_id = bodega.id_bodega, lista_productos = codigo_barras)
                db_inventario.save()
            
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
        mensaje_2 = ""
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
        estado_recepcion_2 = 'pendiente por revision'
        notas_recepcion_2 = ""
        mensaje = ""
        color = ""
        # -- Revision listas para marcar el estado del ingreso -- #

        ## --- Opcion 2, Revision paso a paso --- ##
        if len(lista_organizada_compra) != len(lista_organizada_ingreso):
            if len(lista_organizada_compra) > len(lista_organizada_ingreso):
                
                estado_recepcion_2 = 'pendiente por revision'
                notas_recepcion_2 = "Notas: Faltan productos por recibir."
                mensaje = "Recepción realizada"
                mensaje_2 = "¡Faltan productos por recibir!"
                color = "#c42727"
                # Se pueden almancenar en variable para luego notificar al usuario
            elif len(lista_organizada_compra) < len(lista_organizada_ingreso):
                
                estado_recepcion_2 = 'pendiente por revision'
                notas_recepcion_2 = "Notas: Se recibieron productos de más."
                mensaje = "Recepción realizada"
                mensaje_2 = "¡Se recibieron productos de más!"
                color = "#c42727"
                # Se pueden almacenar en variable para luego notificar al usuario
        else:
            if lista_organizada_compra == lista_organizada_ingreso:
                
                estado_recepcion_2 = 'OK'
                notas_recepcion_2 = "Notas: Todo en orden. Productos y cantidades coinciden."
                mensaje = "Recepción realizada satisfactoriamente"
                mensaje = "¡Todo en orden!"
                color = "#2bb52b"
            else:
                estado_recepcion_2 = 'pendiente por revision'
                notas_recepcion_2 = "Notas: Los productos recibidos no coinciden con los comprados."
                mensaje = "Recepción realizada"
                mensaje_2 = "¡Los productos recibidos no coinciden con los comprados!"
                color = "#c42727"
        
        db_recepcion = Recepcion(id_compra_id=id_compra, id_bodega_id=id_bodega, id_empleado_id=usuarios_obj.id_empleado, lista_productos=lista_productos, cantidades_productos=cantidades, estado_recepcion=estado_recepcion_2, notas_recepcion=notas_recepcion_2)
        db_recepcion.save()

        inventario_obj = Inventario.objects.get(id_bodega_id = id_bodega)
        ValorDB = inventario_obj.lista_productos
        listaDB = ValorDB.split()
        print(listaDB)

        #ValorFormulario = productos
        #listaFormulario = ValorFormulario.splitlines() #En el codigo de views.py la funcion utilizada debe ser "splitlines()"


        # Sacar claves unicas y frecuencias
        lista_productos_DB = list(Counter(listaDB).keys())
        cantidades_productos_DB = list(Counter(listaDB).values())

        #lista_productos_formulario = list(Counter(listaFormulario).keys())
        #cantidades_productos_formulario = list(Counter(listaFormulario).values())

        # -- Organizar lista recibida de compras -- #
        lista_organizada_DB = list(sorted(zip(lista_productos_DB,cantidades_productos_DB)))
        #lista_organizada_formulario = list(sorted(zip(lista_productos_formulario, cantidades_productos_formulario)))



        for i in range(len(lista_organizada_DB)):
            for z in range(len(lista_organizada_ingreso)):
                if  lista_organizada_DB[i][0] == lista_organizada_ingreso[z][0]:
                    commonItem = list(lista_organizada_DB[i])
                    commonItem[1] += lista_organizada_ingreso[z][1]
                    updatedAmount = tuple(commonItem)
                    lista_organizada_DB[i] = updatedAmount
                    break
                else:
                    continue
        # productos_db = Producto.objects.all()
        # cantidad_para_bodega = 0
        # bodega_2 = Bodega.objects.get(id_bodega = id_bodega)
        '''for producto_db in lista_organizada_DB:
            for producto_2 in productos_db:
                if producto_db[0] == producto_2.codigo_de_barras:
                    lista_productos_inv = producto_2.cantidad.split()
                    lista_productos_inv[bodega_2.id_bodega-1] = str(int(lista_productos_inv[bodega_2.id_bodega-1])+producto_db[1])
                    producto_2.cantidad = lista_productos_inv
                    producto_2.save()
                    cantidad_para_bodega  = cantidad_para_bodega  + producto_db[1]
        
        

        bodega = Bodega.objects.get(id_bodega = id_bodega)  
        bodega.capacidad = bodega.capacidad + cantidad_para_bodega    
        bodega.save()   '''

        updatedList = []
        for producto in lista_organizada_DB:
            for u in range(producto[1]):
                updatedList.append(producto[0])
        
        updatedInventory = " ".join(updatedList)
        print(updatedInventory)
        
        '''db_inventario = Inventario(id_recepcion_id = db_recepcion.id_recepcion, id_bodega_id=id_bodega,lista_productos = updatedInventory)
        db_inventario.save()'''

        compra_obj = Compras.objects.get(id_compra = id_compra)
        compra_obj.estado_compra = 'recibida'
        compra_obj.save()

        inventario_obj_2 = Inventario.objects.get(id_bodega_id = id_bodega)
        inventario_obj_2.lista_productos = updatedInventory
        inventario_obj_2.save()

        db_actividad = Actividad(id_empleado_id=usuarios_obj.id_empleado, tipo_actividad='ingreso productos')
        db_actividad.save()

        compras_obj = Compras.objects.filter(estado_compra='por recibir')
        return render(request, 'ingreso_productos.html', {'compras': compras_obj, 'mensaje': mensaje, 'mensaje_2':mensaje_2, 'color_mensaje':color})

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
    

@login_required(login_url='../login/')
def despacho_productos(request):
    usuarios_obj = Empleado.objects.get(nombre=request.user)
    try:
        id_bodega = request.POST['id_bodega']
        id_venta = request.POST['id_venta']
        productos = request.POST['productos']
    except:
        ventas_obj = Ventas.objects.filter(estado_venta='por entregar')
        bodegas_obj = Bodega.objects.all()
        return render(request, 'despacho_productos.html', {'ventas': ventas_obj, 'mensaje': '', 'bodegas': bodegas_obj})
    else:

        #Elementos que vienen de la base de datos
        venta_objeto = Ventas.objects.get(id_venta=id_venta)
        str_pr_venta = venta_objeto.lista_productos
        lista_pr_venta = str_pr_venta.split()
        print(lista_pr_venta)

        # -- Arreglos de productos y cantidades -- #
        lista_productos_venta = list(Counter(lista_pr_venta).keys())
        cantidades_productos_venta = list(Counter(lista_pr_venta).values())
        # -- Organizar lista recibida de ventas -- #
        lista_organizada_venta = list(sorted(zip(lista_productos_venta,cantidades_productos_venta)))

        #Elementos que salen del formulario
        lista_productos_temp = productos.splitlines()
        
        # -- Areglos de productos y cantidades -- #
        lista_productos = list(Counter(lista_productos_temp).keys())
        cantidades = list(Counter(lista_productos_temp).values())

        # -- Organizar lista scaneada para ingresar -- #
        lista_organizada_despacho = list(sorted(zip(lista_productos,cantidades)))
        estado_entrega_2 = 'pendiente por revision'
        notas_entrega_2 = ""
        mensaje = ""
        mensaje_2 = ""
        color = ""
        # -- Revision listas para marcar el estado del despacho -- #

        ## --- Opcion 2, Revision paso a paso --- ##
        if len(lista_organizada_venta) != len(lista_organizada_despacho):
            if len(lista_organizada_venta) > len(lista_organizada_despacho):
                
                estado_entrega_2 = 'pendiente por revision'
                notas_entrega_2 = "Notas: Faltan productos por despachar."
                mensaje = "Despacho fallido"
                mensaje_2 = "¡Faltan productos por despachar!"
                color = "#c42727"
                # Se pueden almancenar en variable para luego notificar al usuario
            elif len(lista_organizada_venta) < len(lista_organizada_despacho):
                
                estado_entrega_2 = 'pendiente por revision'
                notas_entrega_2 = "Notas: Se despacharon productos de más."
                mensaje = "Despacho realizado"
                mensaje_2 = "¡Se despacharon productos de más!"
                color = "#c42727"
                # Se pueden almacenar en variable para luego notificar al usuario
        else:
            if lista_organizada_venta == lista_organizada_despacho:
                
                estado_entrega_2 = 'OK'
                notas_entrega_2 = "Notas: Todo en orden. Productos y cantidades coinciden."
                mensaje = "Despacho realizado satisfactoriamente"
                mensaje = "¡Todo en orden!"
                color = "#2bb52b"
            else:
                estado_entrega_2 = 'pendiente por revision'
                notas_entrega_2 = "Notas: Los productos despachados no coinciden con los vendidos."
                mensaje = "Despacho realizada"
                mensaje_2 = "¡Los productos despachados no coinciden con los vendidos!"
                color = "#c42727"
    

        inventario_obj = Inventario.objects.get(id_bodega_id = id_bodega)
        ValorDB = inventario_obj.lista_productos
        listaDB = ValorDB.split()
        print(listaDB)

        #ValorFormulario = productos
        #listaFormulario = ValorFormulario.splitlines() #En el codigo de views.py la funcion utilizada debe ser "splitlines()"
        

        # Sacar claves unicas y frecuencias
        lista_productos_DB = list(Counter(listaDB).keys())
        cantidades_productos_DB = list(Counter(listaDB).values())

        #lista_productos_formulario = list(Counter(listaFormulario).keys())
        #cantidades_productos_formulario = list(Counter(listaFormulario).values())

        # -- Organizar lista recibida de compras -- #
        lista_organizada_DB = list(sorted(zip(lista_productos_DB,cantidades_productos_DB)))
        #lista_organizada_formulario = list(sorted(zip(lista_productos_formulario, cantidades_productos_formulario)))


        for i in range(len(lista_organizada_DB)):
            for z in range(len(lista_organizada_despacho)):
                if  lista_organizada_DB[i][0] == lista_organizada_despacho[z][0]:
                    commonItem = list(lista_organizada_DB[i])
                    commonItem[1] -= lista_organizada_despacho[z][1]
                    if commonItem[1] < 1:
                        estado_entrega_2 = 'pendiente por revision'
                        notas_entrega_2 = "Notas: Productos insuficientes para despacha."
                        mensaje = "Recepción realizada"
                        mensaje_2 = "¡Faltan productos para completar la orden!"
                        color = "#c42727"
                    updatedAmount = tuple(commonItem)
                    lista_organizada_DB[i] = updatedAmount
                    break
                else:
                    continue

        '''productos_db = Producto.objects.all()
        cantidad_para_bodega = 0
        bodega_2 = Bodega.objects.get(id_bodega = id_bodega)
        for producto_db in lista_organizada_DB:
            for producto_2 in productos_db:
                if producto_db[0] == producto_2.codigo_de_barras:
                    lista_productos_inv = producto_2.cantidad.split()
                    lista_productos_inv[bodega_2.id_bodega-1] = str(int(lista_productos_inv[bodega_2.id_bodega-1])-producto_db[1])
                    producto_2.cantidad = lista_productos_inv
                    producto_2.save()
                    cantidad_para_bodega  = cantidad_para_bodega  - producto_db[1]

        bodega = Bodega.objects.get(id_bodega = id_bodega)  
        bodega.capacidad = bodega.capacidad - cantidad_para_bodega   
        bodega.save()'''

        updatedList = []
        for producto in lista_organizada_DB:
            for u in range(producto[1]):
                updatedList.append(producto[0])
        
        updatedInventory = " ".join(updatedList)
        print(updatedInventory)
        '''db_inventario = Inventario(id_recepcion_id = db_recepcion.id_recepcion, id_bodega_id=id_bodega,lista_productos = updatedInventory)
        db_inventario.save()'''

        db_entrega = Entregas(id_venta_id=id_venta, id_empleado_id=usuarios_obj.id_empleado, lista_productos= lista_productos, cantidades_productos=cantidades, estado_entrega=estado_entrega_2, notas_entrega=notas_entrega_2)
        db_entrega.save()
        
        venta_obj = Ventas.objects.get(id_venta = id_venta)
        venta_obj.estado_venta = 'entregada'
        venta_obj.save()

        inventario_obj_2 = Inventario.objects.get(id_bodega_id = id_bodega)
        inventario_obj_2.lista_productos = updatedInventory
        inventario_obj_2.save()

        db_actividad = Actividad(id_empleado_id=usuarios_obj.id_empleado, tipo_actividad='despacho productos')
        db_actividad.save()

        ventas_obj = Ventas.objects.filter(estado_venta='por entregar')
        bodegas_obj = Bodega.objects.all()

        return render(request, 'despacho_productos.html', {'ventas': ventas_obj, 'bodegas':bodegas_obj,'mensaje': mensaje, 'mensaje_2':mensaje_2, 'color_mensaje':color})


@login_required(login_url='../login/')
def despacho_productos_next(request):
    try:
        id_venta = request.POST['id_venta']
        id_bodega = request.POST['id_bodega']
    except:
        ventas_obj = Ventas.objects.filter(estado_venta='por entregar')
        return render(request, 'despacho_productos.html', {'ventas': ventas_obj})
    else:
        return render(request, 'despacho_productos_next.html', {'id_venta':id_venta, 'id_bodega':id_bodega})
 