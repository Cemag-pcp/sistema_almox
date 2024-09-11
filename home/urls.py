from django.urls import path
from . import views

urlpatterns = [
    path('solicitacoes/', views.lista_solicitacoes, name='lista_solicitacoes'),

    path('processar_edicao/', views.processar_edicao, name='processar_edicao'),

]
