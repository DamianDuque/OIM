from django.db import models

# Create your models here.


class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True, blank=False)
    nombre = models.CharField(max_length=45, null=False)
    rol = models.CharField(max_length=45, null=False, blank=False, choices=(
        ('bodeguero', 'bodeguero'), ('administrador', 'administrador')))
    correo = models.EmailField(max_length=45, null=False, blank=False)


class Producto(models.Model):
	id_producto = models.AutoField(primary_key=True, blank=False)
	codigo_de_barras = models.CharField(max_length=45, null=False)
	nombre = models.CharField(max_length=45, null=False)
	descripcion = models.CharField(max_length=100, null=False)
	peso = models.PositiveIntegerField(null=False)

class Compras(models.Model):
	id_generico_1 = models.AutoField(primary_key=True, blank=False)
	id_compra = models.CharField(max_length=45, null=False)
	Empleado_id_empleado = models.ForeignKey(
		Empleado, null=False, blank=False, on_delete=models.CASCADE)
	proveedor = models.CharField(max_length=45, null=False)
	Producto_id_producto = models.ForeignKey(
		Producto, null=False, blank=False, on_delete=models.CASCADE)
	cantidad_producto = models.PositiveIntegerField(default=0)
	total_compra = models.PositiveIntegerField(default=0)


class Recepcion(models.Model):
	Compras_id_generico_1 = models.ForeignKey(
		Compras, null=False, blank=False, on_delete=models.CASCADE)
	id_generico_2 = models.AutoField(primary_key=True, blank=False)
	id_recepcion = models.CharField(max_length=45, null=False)
	Empleado_id_empleado = models.ForeignKey(
		Empleado, null=False, blank=False, on_delete=models.CASCADE)
	Producto_id_producto = models.ForeignKey(
		Producto, null=False, blank=False, on_delete=models.CASCADE)
	cantidad_producto = models.PositiveIntegerField(default=0)
	fecha_ingreso = models.DateTimeField(auto_now_add=True)
	estado_recepcion = models.CharField(max_length=45, null=False, blank=False, choices=(
		('por recibir', 'por recibir'), ('recibido', 'recibido'), ('pendiente por revision', 'pendiente por revision')))
	notas_recepcion = models.CharField(max_length=45, null=False)


class Ventas(models.Model):
	id_generico_3 = models.AutoField(primary_key=True, blank=False)
	id_venta = models.CharField(max_length=45, null=False)
	Empleado_id_empleado = models.ForeignKey(
		Empleado, null=False, blank=False, on_delete=models.CASCADE)
	cliente = models.CharField(max_length=45, null=False)
	Producto_id_producto = models.ForeignKey(
		Producto, null=False, blank=False, on_delete=models.CASCADE)
	cantidad_producto = models.PositiveIntegerField(default=0)
	total_venta = models.PositiveIntegerField(default=0)


class Entregas(models.Model):
	Ventas_id_generico_3 = models.ForeignKey(
		Ventas, null=False, blank=False, on_delete=models.CASCADE)
	id_generico_4 = models.AutoField(primary_key=True, blank=False)
	id_entrega = models.CharField(max_length=45, null=False)
	Empleado_id_empleado = models.ForeignKey(
		Empleado, null=False, blank=False, on_delete=models.CASCADE)
	Producto_id_producto = models.ForeignKey(
		Producto, null=False, blank=False, on_delete=models.CASCADE)
	cantidad_producto = models.PositiveIntegerField(default=0)
	fecha_despacho = models.DateTimeField(auto_now_add=True)
	estado_entrega = models.CharField(max_length=45, null=False, blank=False, choices=(
		('por entregar', 'por entregar'), ('entregado', 'entregado'), ('pendiente por revision', 'pendiente por revision')))
	notas_entrega = models.CharField(max_length=45, null=False)


class Inventario(models.Model):
	id_generico_5 = models.AutoField(primary_key=True, blank=False)
	Recepcion_id_generico_2 = models.ForeignKey(
		Recepcion, null=True, blank=True, on_delete=models.CASCADE)
	id_bodega = models.PositiveIntegerField(null=False)
	Producto_id_producto = models.ForeignKey(
		Producto, null=False, blank=False, on_delete=models.CASCADE)
	cantidad_producto = models.PositiveIntegerField(default=0)
