import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from solicitacao.models import SolicitacaoTransferencia
from cadastro.models import Funcionario,DepositoDestino,ItensTransferencia,Operador

"""

Crie um arquivo CSV com as colunas: quantidade | obs | data_entrega	| deposito_destino_id |	funcionario_id | item_id | entregue_por_id

Nome do arquivo: transferencias_erica.csv
Import na raiz do projeto e roda o seguinte comando:
python manage.py import_transferencias_prontas

"""

class Command(BaseCommand):
    help = 'Importa itens de transferência do arquivo CSV'

    def handle(self, *args, **kwargs):
        try:
            with open('transferencias_erica.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    try:
                        # Buscar ou verificar as chaves estrangeiras
                        funcionario = Funcionario.objects.get(id=int(row['funcionario_id']))
                        deposito_destino = DepositoDestino.objects.get(id=int(row['deposito_destino_id']))
                        item = ItensTransferencia.objects.get(codigo=row['item_id'])
                        entregue_por = None

                        # Tratar a possibilidade de `entregue_por_id` ser nulo
                        if row['entregue_por_id']:
                            entregue_por = Operador.objects.get(id=int(row['entregue_por_id']))

                        # Converter os valores restantes
                        quantidade = float(row['quantidade'])
                        obs = row['obs']
                        data_entrega = None
                        if row['data_entrega']:
                            data_entrega = datetime.strptime(row['data_entrega'], '%Y-%m-%d %H:%M:%S.%f %z')
                        rpa = row.get('rpa', None)

                        # Criar a instância no banco de dados
                        SolicitacaoTransferencia.objects.create(
                            funcionario=funcionario,
                            deposito_destino=deposito_destino,
                            item=item,
                            quantidade=quantidade,
                            obs=obs,
                            data_entrega=data_entrega,
                            entregue_por=entregue_por,
                            rpa=rpa
                        )

                        self.stdout.write(self.style.SUCCESS(f'Transferência criada com sucesso para {funcionario} - {item}'))

                    except Funcionario.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Funcionario não encontrado: {row["funcionario_id"]}'))
                    except DepositoDestino.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'DepositoDestino não encontrado: {row["deposito_destino_id"]}'))
                    except ItensTransferencia.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Item não encontrado: {row["item_id"]}'))
                    except Operador.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Operador não encontrado: {row["entregue_por_id"]}'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao processar a linha {row}: {e}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Arquivo CSV não encontrado. Verifique o caminho e tente novamente.'))

