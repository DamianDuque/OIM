# Generated by Django 4.0.6 on 2023-05-22 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MGYP', '0005_alter_producto_peso'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id_generico_6', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_actividad', models.CharField(choices=[('nuevo producto', 'nuevo producto'), ('ingreso productos', 'ingreso productos'), ('despacho productos', 'despacho productos')], max_length=45)),
                ('fecha_actividad', models.DateTimeField(auto_now_add=True)),
                ('Empleado_id_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MGYP.empleado')),
            ],
        ),
    ]