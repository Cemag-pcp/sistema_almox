# Generated by Django 5.0.6 on 2024-10-18 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0006_remove_funcionario_cc_funcionario_cc'),
    ]

    operations = [
        migrations.AddField(
            model_name='itenstransferencia',
            name='unidade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='itenssolicitacao',
            name='unidade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]