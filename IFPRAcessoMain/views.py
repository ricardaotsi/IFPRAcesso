"""
Imports
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from IFPRAcessoMain.models import Identificador
from django.http import JsonResponse


@login_required
def pesquisa(request):
    """
    Tela pesquisa
    """
    return render(request, "IFPRAcessoMain/pesquisa.html")

@login_required
def insertId(request):
    """
    Tela inserir Identificador
    """
    todos_id = Identificador.objects.all()
    return render(request, "IFPRAcessoMain/insertId.html", {'todos_id':todos_id})

@login_required
def deleteId(request):
    """
    Função Ajax que deleta um identificador do banco
    """
    identificardor = request.GET.get('identificador', None)
    Identificador.objects.filter(nome_id=identificardor.strip()).delete()
    data = {}
    return JsonResponse(data)
