from django.urls import path
from . import views

urlpatterns = [
    path('criar-solicitacoes/', views.criar_solicitacoes, name='criar_solicitacoes'),

    path('ajax/get-cc/', views.get_cc_by_matricula, name='get_cc_by_matricula'),
    path('ajax/get-unidade/', views.get_unidade_by_item, name='get_unidade_by_item'),
    path('ajax/carregar-classes/', views.carregar_classes, name='ajax_carregar_classes'),

    path('historico/requisicao', views.historico_requisicao, name='historico_requisicao'),
    path('historico/processa-historico-requisicao/', views.solicitacao_data_requisicao, name='solicitacao_data_requisicao'),
    
    path('historico/transferencia', views.historico_transferencia, name='historico_transferencia'),
    path('historico/processa-historico-transferencia/', views.solicitacao_data_transferencia, name='solicitacao_data_transferencia'),

    path('cadastrar-novo-item/', views.cadastro_novo_item, name='cadastro_novo_item'),
    path('cadastrar-nova-matricula/', views.cadastro_nova_matricula, name='cadastro_nova_matricula'),

    path('gerir-solicitacao-cadastro/', views.gerir_solicitacoes, name='gerir_solicitacoes'),
    
    path('cadastro-item/edit/<int:pk>/<str:tipo_cadastro>', views.edit_solicitacao_cadastro_item, name='edit_solicitacao_cadastro_item'),
    path('cadastro-item/edit/<int:pk>', views.edit_solicitacao_cadastro_matricula, name='edit_solicitacao_cadastro_matricula'),


]