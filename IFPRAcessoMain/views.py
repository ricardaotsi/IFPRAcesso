"""
Imports
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db import IntegrityError
from IFPRAcessoMain.models import Identificador, Pessoa



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
        id_post=Identificador(nome_id=request.POST.get('identificador'))
        id_post.nome_id=id_post.nome_id.upper()
        try:
            id_post.save()
            messages.success(request, 'Identificador inserido com sucesso')
        except Exception as e:
            if isinstance(e, IntegrityError):
                messages.error(request, 'Identificador já existe')
            else:
                messages.error(request, 'Ocorreu um problema no cadastro do Identificador')
        return HttpResponseRedirect("/insertId/")
    else:
        todos_id = Identificador.objects.all().order_by('nome_id')
        return render(request, "IFPRAcessoMain/insertId.html", {'todos_id':todos_id})

@login_required
def deleteId(request):
    """
    Função Ajax que deleta um identificador do banco
    """
    temp_id = Identificador.objects.filter(nome_id=request.GET.get('identificador', None))
    resultado = False
    try:
        temp_id.delete()
        resultado = True
    except Exception:
        resultado = False
    data = {
        'resultado': resultado
    }
    return JsonResponse(data)

@login_required
def insertPessoa(request):
    """
    Tela inserir Pessoa
    """
    todos_id = Identificador.objects.all().order_by('nome_id')
    if request.method == 'POST':
        pessoa=Pessoa()
        pessoa.nome_pessoa = request.POST.get('nome').upper()
        pessoa.id_pessoa = Identificador.objects.get(nome_id=request.POST.get('identificador'))
        pessoa.cracha_pessoa = request.POST.get('cracha')
        pessoa.matricula_pessoa = request.POST.get('matricula')
        pessoa.ano_entrada = request.POST.get('ano')
        pessoa.ativo = request.POST.get('ativo')
        try:
            pessoa.save()
            messages.success(request, 'Pessoa inserida com sucesso')
        except Exception as e:
            if isinstance(e, IntegrityError):
                erro = "Cadastro não realizado:"
                if Pessoa.objects.filter(nome_pessoa=pessoa.nome_pessoa).exists():
                    erro = erro+' | Pessoa já existe'
                if Pessoa.objects.filter(cracha_pessoa=pessoa.cracha_pessoa).exists():
                    erro = erro+' | Cracha já existe'
                if Pessoa.objects.filter(matricula_pessoa=pessoa.matricula_pessoa).exists():
                    erro = erro+' | Matricula já existe'
                messages.error(request, erro+" |")
            else:
                messages.error(request, 'Ocorreu um problema no cadastro da Pessoa')
            request.session['nome'] = pessoa.nome_pessoa
            request.session['cracha'] = pessoa.cracha_pessoa
            request.session['matricula'] = pessoa.matricula_pessoa
            request.session['ano'] = pessoa.ano_entrada
            request.session['identificador'] = str(pessoa.id_pessoa)
            return render(request, "IFPRAcessoMain/insertPessoa.html", {'todos_id':todos_id, 
                                                                        'nome':request.session['nome'],
                                                                        'cracha':request.session['cracha'],
                                                                        'matricula':request.session['matricula'],
                                                                        'ano':request.session['ano'],
                                                                        'identificador':request.session['identificador']})
        return HttpResponseRedirect("/pessoa/")
    else:
        return render(request, "IFPRAcessoMain/insertPessoa.html", {'todos_id':todos_id})