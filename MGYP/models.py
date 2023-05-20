from django.db import models

# Create your models here.

class Empleado(models.Model):
	id_empleado = models.AutoField(primary_key=True, blank=False)
	nombre = models.CharField(max_length=45, null=False)
	rol = models.CharField(max_length=45, null=False, blank=False, choices=(('bodeguero','bodeguero'),('administrador','administrador')))
	correo = models.EmailField(max_length=45, null=False, blank=False)