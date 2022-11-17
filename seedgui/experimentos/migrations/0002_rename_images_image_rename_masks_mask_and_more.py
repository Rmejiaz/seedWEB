# Generated by Django 4.1.2 on 2022-11-17 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experimentos', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Images',
            new_name='Image',
        ),
        migrations.RenameModel(
            old_name='Masks',
            new_name='Mask',
        ),
        migrations.AddField(
            model_name='experimento',
            name='status',
            field=models.CharField(default='Finalizado', max_length=20),
            preserve_default=False,
        ),
    ]
