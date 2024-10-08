# Generated by Django 4.2.15 on 2024-08-30 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0003_operador_status'),
        ('solicitacao', '0005_solicitacaorequisicao_rpa_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacaoCadastroItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_solicitacao', models.CharField(max_length=20)),
                ('codigo', models.CharField(blank=True, max_length=100, null=True)),
                ('descricao', models.CharField(blank=True, max_length=100, null=True)),
                ('quantidade', models.IntegerField()),
                ('aprovado', models.BooleanField(default=False)),
                ('data_aprovacao', models.DateTimeField(blank=True, null=True)),
                ('deposito_destino', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitacao_deposito_destino', to='cadastro.depositodestino')),
                ('funcionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cadastro_item', to='cadastro.funcionario')),
            ],
        ),
    ]
