# Generated by Django 4.0.6 on 2023-05-25 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGYP', '0035_alter_entregas_notas_entrega_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='cantidad',
            field=models.CharField(max_length=5000),
        ),
    ]
