import csv
from django.core.management.base import BaseCommand
from cadastro.models import ItensTransferencia

"""

Crie um arquivo CSV com as colunas: Descrição | Código | Un.

Código: Obrigatório
Descrição: Opcional
Un.: Opcional

Nome do arquivo: itens_transferencia.csv
Import na raiz do projeto e roda o seguinte comando:
python manage.py import_itens_transferencia

"""

class Command(BaseCommand):
    help = 'Importa itens de transferência do arquivo CSV'

    def handle(self, *args, **kwargs):
        with open('itens_transferencia.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                codigo = row['Código']
                nome = row['Descrição']
                unidade = row['Un.']

                item, created = ItensTransferencia.objects.get_or_create(
                    codigo=codigo,
                    defaults={'nome': nome, 'unidade': unidade}
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Item {codigo} - {nome} importado com sucesso.'))
                else:
                    self.stdout.write(self.style.WARNING(f'Item {codigo} já existe no banco de dados.'))

