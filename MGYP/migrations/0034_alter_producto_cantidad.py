# Generated by Django 4.0.6 on 2023-05-25 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGYP', '0033_producto_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
    ]
