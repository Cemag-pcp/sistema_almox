# Generated by Django 5.0.4 on 2024-09-12 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0003_operador_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='matricula',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]