from django.urls import path

from . import views
from .views import CustomLogoutView

urlpatterns = [
    path('solicitacoes/', views.lista_solicitacoes, name='lista_solicitacoes'),

    path('processar_edicao/', views.processar_edicao, name='processar_edicao'),

    path('login/', views.user_login, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
]
