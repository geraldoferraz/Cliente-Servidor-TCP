import socket
from datetime import datetime
from utils import BUFFER_SIZE, PORT
from threading import Thread

class Server:   

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('127.0.0.1', PORT))
        self.server_socket.listen(5)  # Permite até 5 conexões não aceitas antes de começar a rejeitar novas. Ajuste conforme necessário.

        self.dict_users = {}    # mapeando socket -> username
        self.map_adr_pkt = {}   # mapeando user -> pacote esperado

        # Inicia a thread para aceitar conexões. Cada conexão terá sua própria thread.
        self.accept_thread = Thread(target=self.accept_connections)
        self.accept_thread.start()

    def accept_connections(self):
        while True:
            # Aceita uma nova conexão
            client_socket, client_address = self.server_socket.accept()
            print(f"Conexão de {client_address} foi estabelecida!")

            # Inicia uma nova thread para lidar com a comunicação com esse cliente
            handle_thread = Thread(target=self.handle_client, args=(client_socket,))
            handle_thread.start()

    def handle_client(self, client_socket):
        while True:
            try:
                # Recebe dados do cliente
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break  # Se não receber dados, a conexão foi fechada

                data = data.decode()
                client_address = client_socket.getpeername()

                # Aqui você colocaria o resto da lógica que estava em seu método 'send'
                # mas adaptada para o contexto de uma conexão TCP única.
                # ...
                # Por exemplo:
                if not (client_socket in self.dict_users):
                    # Adiciona o usuário aos dicionários da classe
                    data = self.hi(data, client_address)
                    self.dict_users[client_socket] = data[16:]  # ou qualquer lógica que você estava usando para extrair o nome de usuário
                    self.map_adr_pkt[client_socket] = '0'
                
                # ... resto da lógica ...

            except Exception as e:
                print(f"Exceção: {e}")
                break

        # Limpa quando o cliente se desconectar
        client_socket.close()
        print(f"Conexão com {client_address} foi fechada!")

    # ... seus outros métodos ...

# Inicia o servidor
test = Server()
