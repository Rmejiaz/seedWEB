# Generated by Django 4.1.2 on 2022-11-17 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentos', '0004_alter_experimento_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimento',
            name='cantidad_imagenes',
            field=models.IntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='experimento',
            name='fecha_inicio',
            field=models.DateTimeField(blank=True, editable=False),
        ),
    ]
