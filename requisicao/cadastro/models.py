from django.db import models
from django.contrib import admin

class Cc(models.Model):

    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):

        return f'{self.nome}'
    

class Funcionario(models.Model):

    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=5)
    cc = models.ForeignKey(Cc, on_delete=models.CASCADE, related_name='funcionario_cc')

    def __str__(self):

        return f'{self.nome} - {self.matricula} - {self.cc.nome}'

class ItensSolicitacao(models.Model):

    CLASSE_CHOICES = (('Req p Consumo', 'Consumo'),
                      ('Req p Produção', 'Produção'))
    
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)
    classe_requisicao = models.CharField(max_length=20, choices=CLASSE_CHOICES)
    unidade = models.CharField(max_length=10)

    def __str__(self):

        return f'{self.codigo} - {self.nome}'
    
class ItensTransferencia(models.Model):

    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100)

    def __str__(self):

        return f'{self.codigo} - {self.nome}'

class DepositoDestino(models.Model):

    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):

        return f'{self.nome}'
 
class Operador(models.Model):

    matricula = models.CharField(max_length=5, unique=True)
    nome = models.CharField(max_length=100)
    status = models.BooleanField(default=True)    

    def __str__(self):

        return f'{self.matricula} - {self.nome}'

class FuncionarioAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'matricula', 'cc__nome']

class ItensSolicitacaoAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'nome', 'classe_requisicao']

class ItensTransferenciaAdmin(admin.ModelAdmin):
    search_fields = ['codigo', 'nome']

class DepositoDestinoAdmin(admin.ModelAdmin):
    search_fields = ['nome']