# Generated by Django 4.1.2 on 2022-11-17 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentos', '0005_alter_experimento_cantidad_imagenes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimento',
            name='fecha_inicio',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
    ]
