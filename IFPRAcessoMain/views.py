""" Imports """
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed, HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Max
from IFPRAcessoMain.models import Identificador, Pessoa
import socket

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

def textFormat(data):
    aux2=""
    BYTE_TAM=[]
    BYTE_INIT = chr(int("2", base=16))#conf. bit inicial
    BYTE_END = chr(int("3", base=16))#conf. bit final
    BYTE_TAM.append(chr(len(data)))#conf. tamanho dos dados
    BYTE_TAM.append(chr(int("0", base=16)))
    aux2 += BYTE_INIT#Inserindo byte inicial
    aux2 += BYTE_TAM[0]#Inserindo byte do tamanho
    aux2 += BYTE_TAM[1]
    aux = aux2+data# concatenando com a informação
    BYTE_CKSUM = aux[1]#Calculo do Checksum
    for a in range(2,len(aux)):
        BYTE_CKSUM = chr(ord(BYTE_CKSUM) ^ ord(aux[a]))
    aux += BYTE_CKSUM#Inserindo Checksum
    aux += BYTE_END#Inserindo byte Final
    return aux

def catraca(matricula, nome, cracha, operacao):
    TCP_IP = ['172.17.150.1',
                '172.17.150.2',
                '172.17.150.3',
                '172.17.150.4']
    TCP_PORT = 3000
    BUFFER_SIZE = 1024
    MESSAGE = "01+ECAR+00+1+"+operacao+"["+str(matricula)+"["+str(matricula)+"[[[1[1[1[[[[W[2[1[1[0[[0["+nome+"["+str(cracha)+"["
    response = []
    for ip in TCP_IP:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, TCP_PORT))
            s.send(textFormat(MESSAGE).encode())
            data = s.recv(BUFFER_SIZE).decode()
            if data.split("+")[4].startswith("0*"):
                if operacao == "I":
                    response.append('Registro inserido com sucesso na Catraca '+ip[-1])
                elif operacao == "A":
                    response.append('Registro alterado com sucesso na Catraca '+ip[-1])
                elif operacao == "E":
                    response.append('Registro removido com sucesso na Catraca '+ip[-1])
            else:
                if operacao == "I":
                    response.append('Houve um problema de cadastro na Catraca '+ip[-1]+'. Cadastre manualmente')
                elif operacao == "A":
                    response.append('Houve um problema de alteração na Catraca '+ip[-1]+'. Altere manualmente')
                elif operacao == "E":
                    response.append('Houve um problema de remoção na Catraca '+ip[-1]+'. Altere manualmente')
        except Exception as e:
            response.append('Catraca '+ip[-1]+' está offline')
        s.close()
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
            #Insere registros nas catracas usando socket
            response = catraca(pessoa.matricula_pessoa,pessoa.nome_pessoa,pessoa.cracha_pessoa,"I")
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
        if Pessoa.objects.filter(matricula_pessoa=pessoa.cracha_pessoa).exists():
            messages.error(request, 'Cracha não pode ser igual a uma matrícula já cadastrada')
            return HttpResponseRedirect("/pessoa/?identificador="+str(pessoa.id_pessoa)+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+str(pessoa.matricula_pessoa)+
                                        "&ano="+pessoa.ano_entrada+
                                        "&ativo="+pessoa.ativo)
        try:
            pessoa.save()
            messages.success(request, 'Pessoa alterada com sucesso.')
            #Altera registros nas catracas usando socket
            if pessoa.ativo == "S":
                response = catraca(pessoa.matricula_pessoa,pessoa.nome_pessoa,pessoa.cracha_pessoa,"A")
            elif pessoa.ativo == "N":
                response = catraca(pessoa.matricula_pessoa,pessoa.nome_pessoa,pessoa.cracha_pessoa,"E")
            for r in response:
                if "alterado" in r or "removido" in r:
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
                messages.error(request, erro+" |")
            else:
                messages.error(request, 'Ocorreu um problema no cadastro da Pessoa')
        return HttpResponseRedirect("/pessoa/update/?identificador="+pessoa.id_pessoa.nome_id+
                                        "&nome="+pessoa.nome_pessoa+
                                        "&cracha="+pessoa.cracha_pessoa+
                                        "&matricula="+str(pessoa.matricula_pessoa)+
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

@login_required
def uploadRegistry(request):
    """
    Tela upload de Registros
    Guarda os registros no banco para fácil acesso
    """
    if request.method == 'POST' and request.FILES['registry']:
        registry = []
        for line in request.FILES['registry']:
            registry = line.strip().decode("utf-8").split("[")
            print(registry[3])
            #registry.append(line.strip())
        #print(registry)
    return render(request, "IFPRAcessoMain/uploadRegistry.html")