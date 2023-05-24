# Generated by Django 4.0.6 on 2023-05-24 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGYP', '0021_bodega'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodega',
            name='capacidad_max',
            field=models.PositiveIntegerField(default=2000),
        ),
        migrations.AlterField(
            model_name='bodega',
            name='capacidad',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
