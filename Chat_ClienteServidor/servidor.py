import socket as sock
import threading

# LISTA PARA ARMAZENAR O SOCKET DOS CLIENTES
lista_clientes = []
clientes = {}  

# ENVIAR MENSAGEM PARA TODOS OS CLIENTES DA LISTA
def broadcast(mensagem,remetente_socket=None):
    for cliente in lista_clientes:
        if cliente != remetente_socket:
            try:
                cliente.sendall(mensagem.encode())
            except:
                # Remover o cliente da lista se houver um erro ao enviar a mensagem
                lista_clientes.remove(cliente)

def mensagem_privada(remetente, destinatario, mensagem):
    # Envia uma mensagem privada para um cliente específico, se ele existir
    if destinatario in clientes:
        try:
            clientes[destinatario].sendall(f"[Privado de {remetente}]: {mensagem}".encode())
            return True
        except:
            lista_clientes.remove(clientes[destinatario])
            del clientes[destinatario]
    return False

def recebe_mensagem(sock_conn, ender):
     #antes de entrarmos no loop, vamos receber o nome
     nome = sock_conn.recv(50).decode()
     print(f"Conexão com {nome} - {ender}")
      # Adicionar o nome e o socket do cliente ao dicionário e à lista
     clientes[nome] = sock_conn
     lista_clientes.append(sock_conn)
     broadcast(f"{nome} entrou no chat!")
     while True:
            try:
                #recebimento da mensagem
                mensagem = sock_conn.recv(1024).decode()
                print(f"{nome} enviou: {mensagem}")
                 # Verificar se é uma mensagem privada
                if mensagem.startswith("@"):
                    try:
                        nome_destino, mensagem_priv = mensagem[1:].split(" ", 1)
                        if not mensagem_privada(nome, nome_destino, mensagem_priv):
                            sock_conn.sendall("Usuário não encontrado ou mensagem privada falhou.".encode())
                    except ValueError:
                        sock_conn.sendall("Formato inválido. Use @<nome_destino> <mensagem>".encode())
                else:
                    # Broadcast da mensagem para todos os outros clientes
                    broadcast(f"{nome}: {mensagem}")
            except: 
                # Notificar todos sobre a saída do cliente
                lista_clientes.remove(sock_conn)
                if nome in clientes:
                    del clientes[nome]
                broadcast(f"{nome} saiu do chat.")
                sock_conn.close()
                break

HOST = '127.0.0.1' #localhosst (servidor)
PORTA = 9999
#sock.AF_INET : IPv4
#sock.SOCK_STREAM : Transporte via TCP

#criamos o socket de conexão com o servidor
sock_server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
#bind -> linkar HOST a PORTA
sock_server.bind((HOST,PORTA))
#servidor entra no modo de escuta
sock_server.listen()
print(f"O servidor {HOST}:{PORTA} está aguardando conexões...")

#o accept retorna o socket de conexão com cliente (conn)
#e retorna o endereço do cliente
#Criamos nosso loop principal para aceitar vários clientes
while True:
        conn, ender = sock_server.accept()
        threadCliente =threading.Thread(target=recebe_mensagem, args=[conn, ender])
        threadCliente.start()