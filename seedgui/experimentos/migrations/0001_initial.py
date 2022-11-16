# Generated by Django 4.1.2 on 2022-11-16 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_final', models.DateTimeField()),
                ('frecuencia', models.IntegerField()),
                ('cantidad_imagenes', models.IntegerField()),
                ('observaciones', models.CharField(max_length=200)),
                ('cantidad_semillas', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Semillas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('germinadas', models.IntegerField()),
                ('no_germinadas', models.IntegerField()),
                ('experimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experimentos.experimento')),
            ],
        ),
        migrations.CreateModel(
            name='Masks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mask', models.ImageField(upload_to='masks')),
                ('fecha', models.DateField()),
                ('experimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experimentos.experimento')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='pics')),
                ('fecha', models.DateField()),
                ('experimento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experimentos.experimento')),
            ],
        ),
    ]
