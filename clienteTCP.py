import socket
from threading import Thread, Lock
from time import time

BUFFER_SIZE = 1024  # Ajuste conforme necessário
IP = '127.0.0.1'  #como o cliente ta sendo executado na mesma maquina do servidor, nos podemos utilizar esse ip padrao 
PORT = 12345  

data_lock = Lock()  # evitar acesso simultâneo a variáveis compartilhadas entre as threads

class Client:
    def __init__(self) -> None:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))  # Estabelece conexão TCP 

        self.sending_thread = Thread(target=self.sending)
        self.receiving_thread = Thread(target=self.receiving)

        self.sending_thread.start()  # iniciando thread de envio de mensagens
        self.receiving_thread.start()  # iniciando thread de recebimento de mensagens

    def sending(self):
        try:
            while True:
                message = input()
                if message == "bye":
                    self.client_socket.close()  # Fecha a conexão se a mensagem for "bye"
                    break
                else:
                    # Envia a mensagem. Não precisamos de um identificador de pacote, já que o TCP garante a ordem
                    self.client_socket.sendall(message.encode())

        except Exception as e:
            print(f"Exception: {e}")
        finally:
            self.client_socket.close()

    def receiving(self):
        try:
            while True:
                # Recebe dados do servidor
                data = self.client_socket.recv(BUFFER_SIZE)
                if not data:
                    # Se não receber dados, a conexão foi fechada
                    print("Conexão fechada pelo servidor")
                    break
                print(data.decode())  # Imprime o que foi recebido do servidor

        except Exception as e:
            print(f"Exception: {e}")
        finally:
            self.client_socket.close()


novo = Client()

# o protocolo de comunicação utilizado é o TCP
# o cliente é capaz de se conectar ao servidor usando o IP do servidor e o número da porta --> isso se encontra na linha 14
# IP é uma string que possui o endereco IP do servidor(que é onde o cliente quer se conectar)
# PORT: Deve ser o número da porta na qual o servidor está escutando. Esse valor deve ser o mesmo no código do servidor e no código do cliente.
