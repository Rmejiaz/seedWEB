# Generated by Django 4.1.2 on 2022-11-17 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentos', '0003_alter_experimento_fecha_inicio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimento',
            name='status',
            field=models.CharField(default='Creado', editable=False, max_length=20),
        ),
    ]
