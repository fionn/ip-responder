#!/usr/bin/env python3

import socket

class Source:
    def __init__(self, token, server_ip = "0.0.0.0", server_port = 10000):
        self.token = token
        self.server_address = (server_ip, server_port)
        self.local_address = ("0.0.0.0", server_port + 1)

    def send(self, token = None):
        token = token or self.token
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.sendto(token, self.server_address)
        print("Sent", token.decode(), "to %s:%s" % self.server_address)

    def _receive(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.local_address)

        data = sock.recvfrom(4096)[0]
        return data.decode().split(" ")

    def query(self):
        self.send(self.token + b'?')
        return self._receive()

if __name__ == "__main__":
    token = b"YELLOW SUBMARINE"
    source = Source(token)

    source.send()
    ips = source.query()
    print(ips)

