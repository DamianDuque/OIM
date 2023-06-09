# Generated by Django 4.0.6 on 2023-05-22 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MGYP', '0011_remove_empleado_correo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_actividad', models.CharField(choices=[('nuevo producto', 'nuevo producto'), ('ingreso productos', 'ingreso productos'), ('despacho productos', 'despacho productos')], max_length=45)),
                ('fecha_actividad', models.DateTimeField(auto_now_add=True)),
                ('id_empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MGYP.empleado')),
            ],
        ),
        migrations.DeleteModel(
            name='Historial',
        ),
    ]
