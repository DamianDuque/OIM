# Generated by Django 4.0.6 on 2023-05-24 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MGYP', '0016_compras_fecha_compra'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recepcion',
            name='notas_recepcion',
        ),
    ]
