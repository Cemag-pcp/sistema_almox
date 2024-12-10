from django.core.management.base import BaseCommand
import csv
from solicitacao.models import SolicitacaoTransferencia

class Command(BaseCommand):
    help = 'Atualiza o campo obs de SolicitacaoTransferencia com base em um arquivo CSV'

    def handle(self, *args, **kwargs):
        try:
            with open('itens_update.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    print(row)
                    try:
                        # Buscar a instância pelo ID
                        transferencia = SolicitacaoTransferencia.objects.get(id=int(row['id']))

                        # Atualizar o campo 'obs'
                        transferencia.obs = row['obs']
                        transferencia.save()

                        self.stdout.write(self.style.SUCCESS(f'Atualizado: ID {transferencia.id}, obs: {transferencia.obs}'))

                    except SolicitacaoTransferencia.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f'Registro com ID {row["id"]} não encontrado.'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro ao atualizar ID {row["id"]}: {e}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Arquivo CSV não encontrado. Verifique o caminho e tente novamente.'))
