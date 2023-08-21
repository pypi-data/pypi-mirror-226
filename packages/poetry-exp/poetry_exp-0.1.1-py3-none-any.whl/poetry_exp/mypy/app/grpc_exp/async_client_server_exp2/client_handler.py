# (C) Copyright 2020 Hewlett Packard Enterprise Development Company, L.P.

import grpc


class ClientHandler(object):
    def __init__(self, server, port):
        self.grpc_server = server
        self.grpc_port = port
        self.channel = None

    def create_channel(self):
        channel_address = "{}:{}".format(self.grpc_server, self.grpc_port)
        self.channel = grpc.aio.insecure_channel(channel_address)
        return self.channel

    def close_channel(self):
        self.channel.close()
