# Generated by Django 4.0.6 on 2023-05-24 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MGYP', '0022_bodega_capacidad_max_alter_bodega_capacidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recepcion',
            name='id_bodega',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MGYP.bodega'),
        ),
    ]
