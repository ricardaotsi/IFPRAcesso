""" Imports """
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Max
from IFPRAcessoMain.models import Identificador, Pessoa
import requests
from bs4 import BeautifulSoup
import re


@login_required
def pesquisaPessoa(request):
    """
    Tela inicial pesquisa
    """
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

def insereCatraca(url, headers, q1, q2, q3):
    """Função para adicionar registros nas catracas"""
    if requests.request("GET", url, headers=headers, params=q1).status_code == 200:
        if requests.request("GET", url, headers=headers, params=q2).status_code == 200:
            requests.request("GET", url, headers=headers, params=q3)
            return True
        else:
            return False
    else:
        return False

def alteraCatraca(url, headers, q1, q2, q3,nome,matricula, cracha):
    """Função para alterar registros nas catracas"""
    if requests.request("GET", url, headers=headers, params=q1).status_code == 200:
        response = requests.request("GET", url, headers=headers, params=q2)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            #Find the last <a> element and get it's onclick function. From onClick function get it's last parameter that is int
            idCatraca = re.findall(r'\d+', soup.find_all('a')[-1]['onclick'])[-1]
            altera = {"pgCode":"6","opType":"1","lblId":idCatraca,"lblNameUser":nome,"lblCardID":matricula,"lblRef1":cracha,"lblRef2":"0","lblValIni":"","lblValFim":"","lblAcPass":"","lblPass":"","chkVerDig":"on","cbxCardType":"1","cbxAccessType":"1"}
            if requests.request("GET", url, headers=headers, params=altera).status_code == 200:
                requests.request("GET", url, headers=headers, params=q3)
                return True
            else:
                return False
        else:
            return False
    else:
        return False
            

def catraca(nome_pessoa, matricula_pessoa, cracha_pessoa, tipo):
    """Função para adicionar ou alterar registros nas catracas"""
    url = {"1": "http://172.17.150.1", 
            "2": "http://172.17.150.2/rep.html",
            "3": "http://172.17.150.3", 
            "4": "http://172.17.150.4"}
    entra = {"pgCode":"7","opType":"1","lblId":"0", "lblLogin":"primmesf","lblPass":"121314"}
    insere13 = {"13304":"","pgCode":"6","opType":"1","lblId":"-1","lb01":nome_pessoa,"lb02":matricula_pessoa,"lb03":cracha_pessoa,"lb04":"","lb05":"","lb06":"","lb07":"","lb08":"","chkVerDig":"on","cb00":"1","cb01":"1"}
    insere24 = {"pgCode":"6","opType":"1","lblId":"-1","lblNameUser":nome_pessoa,"lblCardID":matricula_pessoa,"lblRef1":cracha_pessoa,"lblRef2":"","lblValIni":"","lblValFim":"","lblAcPass":"","lblPass":"","chkVerDig":"on","cbxCardType":"1","cbxAccessType":"1"}
    pesquisa = {"pgCode":"12","opType":"1","lblId":"-1","lblRegistration":matricula_pessoa,"lblName":""}
    sai = {"pgCode":"7","opType":"2","lblId":"0"}
    headers = {
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': "172.17.150.2",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }
    response = list()
    if tipo == "insere":
        for index in url:
            if index == "2" or index == "4":
                if insereCatraca(url[index],headers,entra,insere24,sai):
                    response.append('Registro inserido na Catraca '+index)
                else:
                    response.append('Houve um problema de cadastro na Catraca'+index+'. Cadastre manualmente.')
            # else:
            #     if insereCatraca(url[index], headers, entra, insere13, sai):
            #         messages.success(request, 'Registro inserido na Catraca '+index)
            #     else:
            #         messages.error(request, 'Houve um problema de cadastro na Catraca'+index+'. Cadastre manualmente.')
    if tipo == "altera":
        for index in url:
            if index == "2" or index == "4":
                if alteraCatraca(url[index],headers,entra,pesquisa,sai, nome_pessoa, matricula_pessoa, cracha_pessoa):
                    response.append('Registro alterado na Catraca '+index)
                else:
                    response.append('Houve um problema de alteração na Catraca'+index+'. Altere manualmente.')
    return response
  
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
        if pessoa.cracha_pessoa == pessoa.matricula_pessoa:
            messages.error(request, 'Cracha e matrícula não devem ser iguais')
            return HttpResponseRedirect("/pessoa/?identificador="+str(pessoa.id_pessoa)+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+pessoa.matricula_pessoa+
                                        "&ano="+pessoa.ano_entrada+
                                        "&ativo="+pessoa.ativo)
        elif Pessoa.objects.filter(matricula_pessoa=pessoa.cracha_pessoa).exists():
            messages.error(request, 'Cracha não pode ser igual a uma matrícula já cadastrada')
            return HttpResponseRedirect("/pessoa/?identificador="+str(pessoa.id_pessoa)+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+pessoa.matricula_pessoa+
                                        "&ano="+pessoa.ano_entrada+
                                        "&ativo="+pessoa.ativo)
        elif Pessoa.objects.filter(cracha_pessoa=pessoa.matricula_pessoa).exists():
            messages.error(request, 'Matricula não pode ser igual a um cracha já cadastrado')
            return HttpResponseRedirect("/pessoa/?identificador="+str(pessoa.id_pessoa)+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+pessoa.matricula_pessoa+
                                        "&ano="+pessoa.ano_entrada+
                                        "&ativo="+pessoa.ativo)
        try:
            pessoa.save()
            messages.success(request, 'Pessoa inserida com sucesso.')
            #Insere registros nas catracas usando requests
            response = catraca(pessoa.nome_pessoa,pessoa.matricula_pessoa,pessoa.cracha_pessoa, "insere")
            for r in response:
                if "inserido" in r:
                    messages.success(request, r)
                else:
                    messages.error(request, r)
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
        return HttpResponseRedirect("/pessoa/?identificador="+str(pessoa.id_pessoa)+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+pessoa.matricula_pessoa+
                                        "&ano="+pessoa.ano_entrada+
                                        "&ativo="+pessoa.ativo)
    else:
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
        if pessoa.cracha_pessoa == pessoa.matricula_pessoa:
            messages.error(request, 'Cracha e matrícula não devem ser iguais')
            return HttpResponseRedirect("/pessoa/update/?identificador="+pessoa.id_pessoa.nome_id+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+pessoa.matricula_pessoa+
                                        "&ano="+pessoa.ano_entrada+
                                        "&ativo="+pessoa.ativo)
        elif Pessoa.objects.filter(matricula_pessoa=pessoa.cracha_pessoa).exists():
            messages.error(request, 'Cracha não pode ser igual a uma matrícula já cadastrada')
            return HttpResponseRedirect("/pessoa/?identificador="+str(pessoa.id_pessoa)+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+pessoa.matricula_pessoa+
                                        "&ano="+pessoa.ano_entrada+
                                        "&ativo="+pessoa.ativo)
        elif Pessoa.objects.filter(cracha_pessoa=pessoa.matricula_pessoa).exists():
            messages.error(request, 'Matricula não pode ser igual a um cracha já cadastrado')
            return HttpResponseRedirect("/pessoa/?identificador="+str(pessoa.id_pessoa)+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+pessoa.matricula_pessoa+
                                        "&ano="+pessoa.ano_entrada+
                                        "&ativo="+pessoa.ativo)
        try:
            pessoa.save()
            messages.success(request, 'Pessoa alterada com sucesso.')
            #Altera registros nas catracas usando requests
            response = catraca(pessoa.nome_pessoa,pessoa_salva.matricula_pessoa,pessoa.cracha_pessoa, "altera")
            for r in response:
                if "alterado" in r:
                    messages.success(request, r)
                else:
                    messages.error(request, r)
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
