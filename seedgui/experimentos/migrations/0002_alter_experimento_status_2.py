# Generated by Django 4.1.3 on 2023-06-21 16:17

from django.db import migrations
import django_enum_choices.choice_builders
import django_enum_choices.fields
import experimentos.enums


class Migration(migrations.Migration):

    dependencies = [
        ('experimentos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimento',
            name='status_2',
            field=django_enum_choices.fields.EnumChoiceField(choice_builder=django_enum_choices.choice_builders.value_value, choices=[('Active', 'Active'), ('Creted', 'Creted'), ('Finished', 'Finished')], default=experimentos.enums.SetupStatus['activo'], enum_class=experimentos.enums.SetupStatus, max_length=8),
        ),
    ]
