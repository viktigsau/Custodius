# tcp_client.py
import socket
import secrets

HOST = '127.0.0.1'  # Server IP or hostname
PORT = 5597

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("[+] Connected to server")

message = "?CONNECT?"
client_socket.sendall(message.encode())

response = client_socket.recv(1024)
print(f"[Server] {response.decode()}")

response_text = response.decode()

if response_text.startswith("?CONNECT? ACCEPTED"):
    _, _, G, P, Q1 = response_text.split(" ")

    g = int(G[2:])
    p = int(P[2:])
    q1 = int(Q1[2:])

    private_key1 = secrets.randbits(512)

    q2 = pow(g, private_key1, p)

    client_socket.sendall(f"?ENCRYPT? GOOD Q:{q2}".encode("ascii"))

client_socket.close()
