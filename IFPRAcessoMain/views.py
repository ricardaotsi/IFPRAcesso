""" Imports """
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib import messages
from django.db import IntegrityError
from IFPRAcessoMain.models import Identificador, Pessoa



@login_required
def pesquisaPessoa(request):
    """
    Tela inicial pesquisa
    """
    if 'nome' in request.session:
        del request.session['nome']
        del request.session['cracha']
        del request.session['matricula']
        del request.session['ano']
        del request.session['identificador']
        del request.session['ativo']
    todos_id = Identificador.objects.all().order_by('nome_id')
    """If para tratar caso algo seja pesquisado"""
    if request.method == 'POST':
        pesquisa = {
            'id': request.POST.get('identificador'),
            'nome': request.POST.get('nome'),
            'matricula': request.POST.get('matricula'),
            'cracha': request.POST.get('cracha'),
            'ano': request.POST.get('ano'),
            'ativo': request.POST.get('ativo'),
            'inativo': request.POST.get('inativo')
        }
        """ Verifica as váriáveis de pesquisa e retorna um conjunto de pessoas"""
        if pesquisa['id'] is None:
            pesquisa['id'] = ""
        if pesquisa['ativo'] is None and pesquisa['inativo'] is None:
            todas_pessoas = Pessoa.objects.filter(nome_pessoa__icontains=pesquisa['nome'],
                                                    id_pessoa__nome_id__icontains=pesquisa['id'],
                                                    cracha_pessoa__icontains=pesquisa['cracha'],
                                                    matricula_pessoa__icontains=pesquisa['matricula'],
                                                    ano_entrada__icontains=pesquisa['ano'],
                                                    ativo__icontains="None").order_by('nome_pessoa')
        elif pesquisa['ativo'] is not None and pesquisa['inativo'] is not None:
            todas_pessoas = Pessoa.objects.filter(nome_pessoa__icontains=pesquisa['nome'],
                                                    id_pessoa__nome_id__icontains=pesquisa['id'],
                                                    cracha_pessoa__icontains=pesquisa['cracha'],
                                                    matricula_pessoa__icontains=pesquisa['matricula'],
                                                    ano_entrada__icontains=pesquisa['ano']).order_by('nome_pessoa')
        elif pesquisa['ativo'] is None:
            todas_pessoas = Pessoa.objects.filter(nome_pessoa__icontains=pesquisa['nome'],
                                                    id_pessoa__nome_id__icontains=pesquisa['id'],
                                                    cracha_pessoa__icontains=pesquisa['cracha'],
                                                    matricula_pessoa__icontains=pesquisa['matricula'],
                                                    ano_entrada__icontains=pesquisa['ano'],
                                                    ativo__icontains=pesquisa['inativo']).order_by('nome_pessoa')
        elif pesquisa['inativo'] is None:
            todas_pessoas = Pessoa.objects.filter(nome_pessoa__icontains=pesquisa['nome'],
                                                    id_pessoa__nome_id__icontains=pesquisa['id'],
                                                    cracha_pessoa__icontains=pesquisa['cracha'],
                                                    matricula_pessoa__icontains=pesquisa['matricula'],
                                                    ano_entrada__icontains=pesquisa['ano'],
                                                    ativo__icontains=pesquisa['ativo']).order_by('nome_pessoa')
        """Retorna a página de pesquisa com os itens pesquisados"""
        return render(request, "IFPRAcessoMain/pesquisa.html", {'todas_pessoas':todas_pessoas, 'todos_id':todos_id})
    else:
        todas_pessoas = Pessoa.objects.all().order_by('nome_pessoa')
        return render(request, "IFPRAcessoMain/pesquisa.html", {'todas_pessoas':todas_pessoas, 'todos_id':todos_id})

@login_required
def insertId(request):
    """
    Tela inserir Identificador
    Salva um identificador ou retorna erro caso o identificador já exista
    """
    if request.method == 'POST':
        id_post = Identificador(nome_id=request.POST.get('identificador'))
        id_post.nome_id = id_post.nome_id.upper()
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
        """Recebe dados do Form e tenta salvar"""
        pessoa = Pessoa()
        pessoa.nome_pessoa = request.POST.get('nome').upper()
        pessoa.id_pessoa = Identificador.objects.get(nome_id=request.POST.get('identificador'))
        pessoa.cracha_pessoa = request.POST.get('cracha')
        pessoa.matricula_pessoa = request.POST.get('matricula')
        pessoa.ano_entrada = request.POST.get('ano')
        pessoa.ativo = request.POST.get('ativo')
        try:
            pessoa.save()
            messages.success(request, 'Pessoa inserida com sucesso. Aguarde, você será redirecionado automaticamente')
        except Exception as e:
            """Caso o nome, cracha ou matricula já existam, retornar um erro"""
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
            """ Salvar os dados inseridos para retorná-los à tela para facilitar correção"""
            request.session['nome'] = pessoa.nome_pessoa
            request.session['cracha'] = pessoa.cracha_pessoa
            request.session['matricula'] = pessoa.matricula_pessoa
            request.session['ano'] = pessoa.ano_entrada
            request.session['identificador'] = str(pessoa.id_pessoa)
            request.session['ativo'] = pessoa.ativo
    return render(request, "IFPRAcessoMain/insertPessoa.html", {'todos_id':todos_id})

@login_required
def updatePessoa(request):
    """
    Tela para alterar dados da pessoa
    """
    todos_id = Identificador.objects.all().order_by('nome_id')
    if request.method == 'POST':
        """Instancia a pessoa para alteração e insere os novos dados"""
        pessoa_salva = Pessoa.objects.get(pk=request.session['pk'])
        pessoa = Pessoa.objects.get(pk=request.session['pk'])
        pessoa.nome_pessoa = request.POST.get('nome').upper()
        pessoa.id_pessoa = Identificador.objects.get(nome_id=request.POST.get('identificador'))
        pessoa.cracha_pessoa = request.POST.get('cracha')
        pessoa.matricula_pessoa = request.POST.get('matricula')
        pessoa.ano_entrada = request.POST.get('ano')
        pessoa.ativo = request.POST.get('ativo')
        try:
            pessoa.save()
            messages.success(request, 'Pessoa inserida com sucesso. Aguarde, você será redirecionado automaticamente')
        except Exception as e:
            """Caso o nome, cracha ou matricula inseridos já existam, retornar um erro"""
            if isinstance(e, IntegrityError):
                erro = "Alteração não realizada:"
                if Pessoa.objects.filter(nome_pessoa=pessoa.nome_pessoa).exists():
                    if str(pessoa.nome_pessoa) != str(pessoa_salva.nome_pessoa):
                        erro = erro+' | Pessoa já existe'
                if Pessoa.objects.filter(cracha_pessoa=pessoa.cracha_pessoa).exists():
                    if int(pessoa.cracha_pessoa) != int(pessoa_salva.cracha_pessoa):
                        erro = erro+' | Cracha já existe'
                if Pessoa.objects.filter(matricula_pessoa=pessoa.matricula_pessoa).exists():
                    if int(pessoa.matricula_pessoa) != int(pessoa_salva.matricula_pessoa):
                        erro = erro+' | Matricula já existe'
                messages.error(request, erro+" |")
            else:
                messages.error(request, 'Ocorreu um problema no cadastro da Pessoa')
        return HttpResponseRedirect("/pessoa/update/?identificador="+pessoa.id_pessoa.nome_id+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+pessoa.matricula_pessoa+
                                        "&ano="+pessoa.ano_entrada+
                                        "&ativo="+pessoa.ativo)
    else:
        return render(request, "IFPRAcessoMain/updatePessoa.html", {'todos_id':todos_id})

@login_required
def update_session(request):
    """
    Função ajax para salvar um objeto de sessão com o ID de uma pessoa selecionada para alteração, para instanciar o objeto
    """
    resultado = False
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    else:
        request.session['pk'] = Pessoa.objects.get(cracha_pessoa=request.POST.get('cracha', None)).pk
        resultado = True
        data = {
            'resultado':resultado
        }
        return JsonResponse(data)
