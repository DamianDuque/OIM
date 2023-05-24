from django.db import models

# Create your models here.


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True, blank=False)
    nombre = models.CharField(max_length=45, null=False)
    rol = models.CharField(max_length=45, null=False, blank=False, choices=(
        ('bodeguero', 'bodeguero'), ('administrador', 'administrador')))


class Producto(models.Model):
	codigo_de_barras = models.CharField(primary_key=True, unique=True, max_length=45, null=False)
	nombre = models.CharField(max_length=45, null=False)
	descripcion = models.CharField(max_length=100, null=False)
	peso = models.DecimalField(decimal_places=2, max_digits=20, null=False)

class Compras(models.Model):
	id_compra = models.AutoField(primary_key=True, blank=False)
	Empleado_id_empleado = models.ForeignKey(
		Empleado, null=False, blank=False, on_delete=models.CASCADE)
	proveedor = models.CharField(max_length=45, null=False)
	lista_productos = models.CharField(max_length=5000, null=False)
	cantidad_producto = models.CharField(max_length=5000, null=False)
	total_compra = models.PositiveIntegerField(default=0)
	fecha_compra = models.DateTimeField(auto_now_add=False)
	estado_compra = models.CharField(max_length=45, null=False, blank=False, choices=(
		('por recibir', 'por recibir'), ('recibida', 'recibida')))

class Bodega(models.Model):
	id_bodega = models.AutoField(primary_key=True, blank=False)
	capacidad = models.PositiveIntegerField(default= 0, null=False)
	capacidad_max = models.PositiveIntegerField(default= 2000, null=False)
	esta_lleno = models.BooleanField(default= False, null=False)

class Recepcion(models.Model):
	id_compra = models.ForeignKey(
		Compras, null=False, blank=False, on_delete=models.CASCADE)
	id_recepcion = models.AutoField(primary_key=True, blank=False)
	id_bodega = models.ForeignKey(
		Bodega, null=False, blank=False, on_delete=models.CASCADE)
	id_empleado = models.ForeignKey(
		Empleado, null=False, blank=False, on_delete=models.CASCADE)
	lista_productos = models.CharField(max_length=5000, null=False)
	cantidades_productos = models.CharField(max_length=5000, null=False)
	fecha_ingreso = models.DateTimeField(auto_now_add=True)
	estado_recepcion = models.CharField(max_length=45, null=False, blank=False, choices=(
		('OK', 'OK'), ('pendiente por revision', 'pendiente por revision')))
	notas_recepcion = models.CharField(max_length=45, null=False)





class Ventas(models.Model):
	id_venta = models.AutoField(primary_key=True, blank=False)
	id_empleado = models.ForeignKey(
		Empleado, null=False, blank=False, on_delete=models.CASCADE)
	cliente = models.CharField(max_length=45, null=False)
	lista_productos = models.CharField(max_length=5000, null=False)
	cantidades_productos = models.CharField(max_length=5000, null=False)
	total_venta = models.PositiveIntegerField(default=0)


class Entregas(models.Model):
	id_venta = models.ForeignKey(
		Ventas, null=False, blank=False, on_delete=models.CASCADE)
	id_entrega = models.AutoField(primary_key=True, blank=False)
	id_empleado = models.ForeignKey(
		Empleado, null=False, blank=False, on_delete=models.CASCADE)
	lista_productos = models.CharField(max_length=5000, null=False)
	cantidades_productos = models.CharField(max_length=5000, null=False)
	fecha_despacho = models.DateTimeField(auto_now_add=True)
	estado_entrega = models.CharField(max_length=45, null=False, blank=False, choices=(
		('por entregar', 'por entregar'), ('entregado', 'entregado'), ('pendiente por revision', 'pendiente por revision')))
	notas_entrega = models.CharField(max_length=45, null=False)


class Inventario(models.Model):
	id_inventario = models.AutoField(primary_key=True, blank=False)
	id_recepcion = models.ForeignKey(
		Recepcion, null=True, blank=True, on_delete=models.CASCADE)
	id_bodega = models.ForeignKey(
		Bodega, null=False, blank=False, on_delete=models.CASCADE)
	lista_productos = models.CharField(max_length=5000, null=False)
	cantidades_productos = models.CharField(max_length=5000, null=False)
	fecha_ingreso = models.DateTimeField(auto_now_add=True)


class Actividad(models.Model):
	id_empleado = models.ForeignKey(Empleado, null=False, blank=False, on_delete=models.CASCADE)
	tipo_actividad = models.CharField(max_length=45, null=False, blank=False, choices=(
		('nuevo producto', 'nuevo producto'), ('ingreso productos', 'ingreso productos'), ('despacho productos', 'despacho productos')))
	fecha_actividad = models.DateTimeField(auto_now_add=True)