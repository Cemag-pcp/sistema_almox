from django import forms
from .models import SolicitacaoRequisicao, SolicitacaoTransferencia

class SolicitacaoRequisicaoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoRequisicao
        fields = ['funcionario', 'cc', 'item', 'classe_requisicao', 'quantidade', 'obs']

class SolicitacaoTransferenciaForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoTransferencia
        fields = ['funcionario', 'deposito_destino', 'item', 'quantidade', 'obs']
