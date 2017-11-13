#!/usr/bin/env python3

import socket
import ipaddress
import secret

class Source:

    def __init__(self, token, server_ip, server_port):
        self.token = token
        self.server_address = (server_ip, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("", 0))

    def send(self):
        self.sock.sendto(self.token, self.server_address)
        print("Sent \"{}\" to {}:{}".format(self.token.decode(), *self.server_address))

    def _receive(self):
        print("Listening on %s:%s" % self.sock.getsockname())
        data = self.sock.recvfrom(4096)[0]
        return set([ipaddress.ip_address(ip) for ip in data.decode().split()])

    def query(self):
        self.sock.sendto(self.token + b'?', self.server_address)
        print("Getting IPs for \"{}\"".format(self.token.decode()))
        return self._receive()

if __name__ == "__main__":
    source = Source(secret.token, secret.server_ip, secret.server_port)

    source.send()
    ips = source.query()

    for ip in ips:
        print(ip)

