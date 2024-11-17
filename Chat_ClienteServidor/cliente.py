import socket as sock
import threading

HOST = '127.0.0.1' #IP DO SERVIDOR
PORTA = 9999 #PORTA DO SERVIDOR

#CRIAR SOCKET IPV4/TCP
socket_cliente = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

#CLIENTE SOLICITA CONEXÃO
socket_cliente.connect((HOST, PORTA))
print(5 * "*" + "Chat Iniciado" + 5 * "*")

# ENVIANDO O NOME ANTES DE ENTRAR NO LOOP
nome = str(input("Qual seu nome? "))
socket_cliente.sendall(nome.encode())
print("Para sair do chat, digite '/sair'")
print("Para enviar uma mensagem privada, use '@<nome_destino> <mensagem>'")

def receber_mensagens():
    while True:
        try:
            mensagem = socket_cliente.recv(1024).decode()
            if mensagem:
                print(f"\n{mensagem}")
        except:
            print("Erro ao receber mensagem do servidor...")
            socket_cliente.close()
            break

# Iniciar uma thread para receber mensagens do servidor
thread_receber = threading.Thread(target=receber_mensagens)
thread_receber.start()

# CLIENTE ENVIA DADOS PARA O SERVIDOR
while True:
    try:
        mensagem = input('Digite aqui sua mensagem: ')
        if mensagem.lower() == "/sair":
            print("Você saiu do chat.")
            socket_cliente.close()
            break
        socket_cliente.sendall(mensagem.encode())
    except:
        print("Erro no envio...")
        socket_cliente.close()
        break


