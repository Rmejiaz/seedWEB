# Generated by Django 4.1.3 on 2023-06-23 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("experimentos", "0006_petridish"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="petridish",
            options={
                "verbose_name": "Petri Dish",
                "verbose_name_plural": "Petri Dishes",
            },
        ),
        migrations.AddField(
            model_name="experimento",
            name="dish",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="experimentos.petridish",
            ),
            preserve_default=False,
        ),
    ]