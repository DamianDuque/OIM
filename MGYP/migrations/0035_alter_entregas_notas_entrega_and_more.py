# Generated by Django 4.0.6 on 2023-05-25 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGYP', '0034_alter_producto_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregas',
            name='notas_entrega',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='recepcion',
            name='notas_recepcion',
            field=models.CharField(max_length=100),
        ),
    ]
