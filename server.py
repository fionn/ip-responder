#!/usr/bin/env python3

import socket
import sys
import time
from collections import namedtuple

class Sink:

    TOKEN_LENGTH = 16

    def __init__(self):
        self.known_clients = {}

    def add_client(self, client):
        # TODO: accommodate client.token + b'?' here.
        if len(client.token) == self.TOKEN_LENGTH:
            if client.token not in self.known_clients:
                self.known_clients = {client.token: set([client.ip])}
            else:
                self.known_clients[client.token].update([client.ip])

    def listen(self):
        Client = namedtuple("Client", ["token", "ip", "port"])
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('0.0.0.0', 10000)
        sock.bind(server_address)
        print("Listening on %s:%s" % server_address)

        while True:
            data, address = sock.recvfrom(4096)
            print("Received", data.decode(), "from", address[0])
            client = Client(data, address[0], address[1])
            self.add_client(client)
            self.respond(client)

    def respond(self, client):
        """
        This sends the list of IPs the client has connected from to the last IP
        the client has connected from, if the client passes a token matching
        client.token + b"?".
        """
        if len(client.token) == self.TOKEN_LENGTH + 1 and client.token[-1] == 63:
            ips = bytes(" ".join(self.known_clients[client.token[:-1]]), "ascii")
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # We sleep here because the client is (probably) synchronous.
            time.sleep(0.1)
            port = 10001
            sock.sendto(ips, (client.ip, port))
            print("Sent {} to {}:{}".format(ips.decode(), client.ip, port))
        

if __name__ == "__main__":
    Sink().listen()
