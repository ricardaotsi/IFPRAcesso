"""
Imports
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import Error
from django.http import HttpResponseRedirect
from IFPRAcessoMain.models import Identificador



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
    if request.method == 'POST':
        id=Identificador(nome_id=request.POST.get('identificador').upper())
        id.save()
        return HttpResponseRedirect("/insertId/")
    else:
        todos_id = Identificador.objects.all().order_by('nome_id')
        return render(request, "IFPRAcessoMain/insertId.html", {'todos_id':todos_id})

@login_required
def deleteId(request):
    """
    Função Ajax que deleta um identificador do banco
    """
    id_identificador = request.GET.get('id_identificador', None)
    identificador = request.GET.get('identificador', None)
    temp_id = Identificador.objects.filter(id=id_identificador, nome_id=identificador)
    resultado = False
    if temp_id:
        try:
            temp_id.delete()
            resultado = True
        except Error:
            resultado = False
    else:
        resultado = False
    data = {
        'resultado': resultado
    }
    return JsonResponse(data)
