import socket
import threading

HOST='127.0.0.1'
PORT=9090

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

clients=[]
nicknames=[]

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message=client.recv(1024)
            print(f"{nicknames[clients.index(client)]} scrive {message}")
            broadcast(message)
        except:
            index=clients.index(client)
            clients.remove(client)
            client.close()
            nickname=nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address= server.accept()
        print(f"Connected with {str(address)}!")
        client.send("NICK".encode('utf-8'))
        nickname=client.recev(1024)
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nickname del client è {nickname}")
        broadcast(f"{nickname} connesso al server!\n".encode('utf-8'))
        client.send("Connesso al server".encode('utf-8'))
        trhead= threading.Thread(target=handle, args=(client,))
        trhead.start()
print("Server start...")
receive()