import json
import os
import socket
import lib.client_connection as client_conn

CWD = os.getcwd()

CONFIG_FILE = os.path.join(CWD, "config.json")

with open(CONFIG_FILE, "r") as f:
    config: dict[str, str | int] = json.load(f)

# load stuff from the config
HOST = config.get("host", "127.0.0.1")
PORT = config.get("port", 5596)

# init the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[+] Server listening on {HOST}:{PORT}")

connections: list[client_conn.Connection] = []

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Connected by {addr}")

        conn = client_conn.Connection(client_socket, addr)
        conn.start()

        def onclose():
            if conn in connections:
                connections.remove(conn)
        conn.register_onclose(onclose)

        connections.append(conn)
finally:
    print("exiting...")
    
    for conn in connections:
        conn.close()

    server_socket.close()