from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .forms import SolicitacaoRequisicaoForm, SolicitacaoTransferenciaForm
from .models import *
from cadastro.models import Cc

def criar_solicitacoes(request):

    funcionarios = Funcionario.objects.all()
    itens_requisicao = ItensSolicitacao.objects.all()
    itens_transferencia = ItensTransferencia.objects.all()
    depositos_destino = DepositoDestino.objects.all()
    form_requisicao = SolicitacaoRequisicaoForm(request.POST, prefix='requisicao')
    centro_custo = Cc.objects.all()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'requisicao':
            form_requisicao = SolicitacaoRequisicaoForm(request.POST, prefix='requisicao')
            if form_requisicao.is_valid():
                form_requisicao.save()
                return HttpResponseRedirect(reverse('criar_solicitacoes'))  
        
        elif form_type == 'transferencia':
            form_transferencia = SolicitacaoTransferenciaForm(request.POST, prefix='transferencia')
            if form_transferencia.is_valid():
                form_transferencia.save()
                return HttpResponseRedirect(reverse('criar_solicitacoes')) 

    context = {
        'form_requisicao':form_requisicao,
        'depositos':depositos_destino,
        'funcionarios': funcionarios,
        'itens': itens_requisicao,
        'itens_transferencia': itens_transferencia,
        'centro_custo': centro_custo,
    }

    return render(request, 'solicitacao.html', context)

def get_cc_by_matricula(request):
    pk = request.GET.get('matricula')
    funcionario = Funcionario.objects.filter(pk=pk).first()
    if funcionario:
        cc = funcionario.cc.pk

        return JsonResponse({'cc': cc})
    return JsonResponse({'error': 'Funcionário não encontrado'}, status=404)

def get_unidade_by_item(request):
    item_id = request.GET.get('item_id')
    item = ItensSolicitacao.objects.filter(id=item_id).first()
    if item:
        unidade = item.unidade
        return JsonResponse({'unidade': unidade})
    return JsonResponse({'error': 'Item não encontrado'}, status=404)

def historico_requisicao(request):

    return render(request, "historico-requisicao.html")

@csrf_exempt
def solicitacao_data_requisicao(request):
    if request.method == "POST":
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))

        # Ordenação
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')
        
        # Mapeamento do índice da coluna para o campo correspondente no banco de dados
        columns = [
            'classe_requisicao', 
            'quantidade',
            'obs',
            'data_solicitacao', 
            'cc__nome',
            'funcionario__nome',
            'item__nome',
            'entregue_por__nome',
            'data_entrega', 
            'rpa',
        ]
        
        order_column = columns[order_column_index]

        if order_dir == 'desc':
            order_column = '-' + order_column

        # Filtrando as execuções (se houver busca)
        search_value = request.POST.get('search[value]', '')

        solicitacoes = SolicitacaoRequisicao.objects.all()

        if search_value:
            solicitacoes = solicitacoes.filter(
                item__nome__contains=search_value
            )

        # Aplicando ordenação
        solicitacoes = solicitacoes.order_by(order_column)

        # Paginação
        paginator = Paginator(solicitacoes, length)
        solicitacoes_page = paginator.get_page(start // length + 1)

        data = []
        for solicitacao in solicitacoes_page:
            status = "Pendente entrega" if solicitacao.entregue_por is None else "Entregue"
            data.append({
                'classe_requisicao': solicitacao.classe_requisicao,
                'quantidade': solicitacao.quantidade,
                'obs': solicitacao.obs,
                'data_solicitacao': solicitacao.data_solicitacao.strftime("%d/%m/%Y %H:%M"),
                'cc__nome': solicitacao.cc.nome,
                'funcionario__nome': solicitacao.funcionario.nome,
                'item__nome': solicitacao.item.nome,
                'entregue_por__nome': solicitacao.entregue_por.nome if solicitacao.entregue_por else '',
                'ultima_atualizacao': solicitacao.data_solicitacao.strftime("%d/%m/%Y %H:%M"),
                'data_entrega': solicitacao.data_entrega.strftime("%d/%m/%Y %H:%M") if solicitacao.data_entrega else '',
                'status': status,
                'rpa': solicitacao.rpa
            })

        return JsonResponse({
            'draw': draw,
            'recordsTotal': paginator.count,
            'recordsFiltered': paginator.count,
            'data': data,
        })
    
def historico_transferencia (request):

    return render(request, "historico-transferencia.html")

@csrf_exempt
def solicitacao_data_transferencia(request):
    if request.method == "POST":
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))

        # Ordenação
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_dir = request.POST.get('order[0][dir]', 'asc')
        
        # Mapeamento do índice da coluna para o campo correspondente no banco de dados
        columns = [
            'quantidade',
            'obs',
            'data_solicitacao', 
            'deposito_destino__nome',
            'funcionario__nome',
            'item__nome',
            'entregue_por__nome',
            'ultima_atualizacao',
            'data_entrega', 
            'rpa',
        ]
        
        order_column = columns[order_column_index]

        if order_dir == 'desc':
            order_column = '-' + order_column

        # Filtrando as execuções (se houver busca)
        search_value = request.POST.get('search[value]', '')

        solicitacoes = SolicitacaoTransferencia.objects.all()

        if search_value:
            solicitacoes = solicitacoes.filter(
                item__nome__contains=search_value
            )

        # Aplicando ordenação
        solicitacoes = solicitacoes.order_by(order_column)

        # Paginação
        paginator = Paginator(solicitacoes, length)
        solicitacoes_page = paginator.get_page(start // length + 1)

        data = []
        for solicitacao in solicitacoes_page:
            status = "Pendente entrega" if solicitacao.entregue_por is None else "Entregue"
            data.append({
                'quantidade': solicitacao.quantidade,
                'obs': solicitacao.obs,
                'data_solicitacao': solicitacao.data_solicitacao.strftime("%d/%m/%Y %H:%M"),
                'deposito_destino__nome': solicitacao.deposito_destino.nome,
                'funcionario__nome': solicitacao.funcionario.nome,
                'item__nome': solicitacao.item.nome,
                'entregue_por__nome': solicitacao.entregue_por.nome if solicitacao.entregue_por else '',
                'data_entrega': solicitacao.data_entrega.strftime("%d/%m/%Y %H:%M") if solicitacao.data_entrega else '',
                'status': status,
                'rpa': solicitacao.rpa
            })

        return JsonResponse({
            'draw': draw,
            'recordsTotal': paginator.count,
            'recordsFiltered': paginator.count,
            'data': data,
        })

def cadastro_novo_item(request):

    if request.method == 'POST':

        pk_funcionario = request.POST.get('id-funcionario-cadastro-item')
        tipo_solicitacao = request.POST.get('tipo_solicitacao')
        codigo = request.POST.get('id-codigo-item')
        descricao = request.POST.get('id-descricao-item')
        quantidade = request.POST.get('id-quantidade-solicitante')

        funcionario = get_object_or_404(Funcionario, pk=pk_funcionario)

        if tipo_solicitacao == 'transferencia':

            pk_deposito = request.POST.get('id-cadastrar-deposito')

            deposito_destino_object = get_object_or_404(DepositoDestino, pk=pk_deposito)

            SolicitacaoCadastroItem.objects.create(
                funcionario=funcionario,
                tipo_solicitacao=tipo_solicitacao,
                codigo=codigo,
                descricao=descricao,
                quantidade=quantidade,
                deposito_destino=deposito_destino_object
            )

        else:

            SolicitacaoCadastroItem.objects.create(
                funcionario=funcionario,
                tipo_solicitacao=tipo_solicitacao,
                codigo=codigo,
                descricao=descricao,
                quantidade=quantidade,
            )

    return redirect('criar_solicitacoes')

def cadastro_nova_matricula(request):

    if request.method == 'POST':

        matricula = request.POST.get('id-matricula-solicitante')
        nome = request.POST.get('id-nome-solicitante')
        pk_cc = request.POST.get('id-ccusto-solicitante')

        cc_object = get_object_or_404(Cc, pk=pk_cc)

        SolicitacaoNovaMatricula.objects.create(
            matricula=matricula,
            nome=nome,
            cc=cc_object
        )

    return redirect('criar_solicitacoes')

def gerir_solicitacoes(request):

    cadastro_matricula = SolicitacaoNovaMatricula.objects.all()

    cadastro_item = SolicitacaoCadastroItem.objects.all()

    print(request.POST)

    if "apagar" in request.POST:

        tipo_cadastro = request.POST.get("tipo_cadastro")
        solicitacao_id = request.POST.get('id')
        
        print(tipo_cadastro)
        print(solicitacao_id)

        # if tipo_cadastro == 'item':
        #     SolicitacaoCadastroItem.objects.filter(id=solicitacao_id).delete()
        # else:
        #     SolicitacaoNovaMatricula.objects.filter(id=solicitacao_id).delete()

        return redirect("gerir_solicitacoes")

    context = {
        'cadastro_matricula': cadastro_matricula,
        'cadastro_item': cadastro_item
    }

    return render(request, 'solicitacao-cadastro.html', context)