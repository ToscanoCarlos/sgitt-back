# Generated by Django 5.1.1 on 2024-11-01 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_profesor_apellido_materno_profesor_areas_profesor'),
    ]

    operations = [
        migrations.AddField(
            model_name='areaconocimiento',
            name='embedding',
            field=models.BinaryField(null=True),
        ),
        migrations.AddField(
            model_name='materia',
            name='embedding',
            field=models.BinaryField(null=True),
        ),
    ]
