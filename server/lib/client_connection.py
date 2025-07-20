import socket
import threading
import random
import secrets

class Connection:
    def __init__(self, client_socket: socket.socket, addr: tuple[str, int]) -> None:
        self._onclose = []
        self._client_socket = client_socket
        self.addr = addr
        self.active = True
        self._reciv_data = []
        self._private_key1 = secrets.randbits(512)
        self._g = secrets.randbits(256)
        self._p = secrets.randbits(2048)

        self._thread = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self.active = True
        self._thread.start()

    def _loop(self):
        while self.active:
            data = self._client_socket.recv(1024)

            if not data:
                self.close()
                break

            print(f"[Client {self.addr}] {data.decode()}")

            match data:
                case b"?CONNECT?":
                    q = pow(self._g, self._private_key1, self._p)
                    self._send(f"?CONNECT? ACCEPTED G:{self._g} P:{self._p} Q:{q}".encode("ascii"))
                    break
                case _:
                    self._send(f"?ERROR? INVALID".encode("ascii"))
                    break
    
    def _send(self, data: bytes):
        self._client_socket.sendall(data)
    
    def _read(self) -> bytes:
        ...
    
    def close(self):
        for function in self._onclose:
            function()

        self.active = False
        self._client_socket.shutdown(socket.SHUT_RDWR)
        self._client_socket.close()
        print(f"[-] Disconnected {self.addr}")
    
    def register_onclose(self, callback):
        self._onclose.append(callback)