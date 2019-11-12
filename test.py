import socket

def textFormat (data):
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

TCP_IP = ['172.17.150.1',
            '172.17.150.2',
            '172.17.150.3',
            '172.17.150.4']
TCP_PORT = 3000
BUFFER_SIZE = 1024
MESSAGE = "01+ECAR+00+1+E[654321[654321[[[1[1[1[[[[W[2[1[1[0[[0[TESTE[123456["

for ip in TCP_IP:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, TCP_PORT))
        s.send(textFormat(MESSAGE).encode())
        data = s.recv(BUFFER_SIZE).decode()
        
        if data.split("+")[4].startswith("0*"):
            print("certo")
        else:
            print("errado")
    except Exception as e:
        print(e)
        print("errado")
    s.close()



