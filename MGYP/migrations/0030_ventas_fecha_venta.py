# Generated by Django 4.0.6 on 2023-05-25 06:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MGYP', '0029_remove_entregas_cantidades_productos'),
    ]

    operations = [
        migrations.AddField(
            model_name='ventas',
            name='fecha_venta',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
