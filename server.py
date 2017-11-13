#!/usr/bin/env python3

import socket
import time
from collections import namedtuple

class Sink:

    TOKEN_LENGTH = 16

    def __init__(self, port = 10000):
        self.known_clients = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", port))

    def add_client(self, client):
        if len(client.token) >= self.TOKEN_LENGTH:
            token = client.token[:self.TOKEN_LENGTH]
            if token not in self.known_clients:
                self.known_clients = {token: set([client.ip])}
            else:
                self.known_clients[token].update([client.ip])

    def listen(self):
        Client = namedtuple("Client", ["token", "ip", "port"])
        print("Listening on %s:%s" % self.sock.getsockname())

        while True:
            data, address = self.sock.recvfrom(1024)
            print("Received \"{}\" from {}:{}".format(data.decode(), *address))
            client = Client(data, *address)
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
            # We sleep here because the client is (probably) synchronous.
            time.sleep(0.1)
            self.sock.sendto(ips, (client.ip, client.port))
            print("Sent \"{}\" to {}:{}".format(ips.decode(), client.ip, client.port))

if __name__ == "__main__":
    Sink().listen()

