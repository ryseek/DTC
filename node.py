import asyncio
IP = "127.0.0.1"
Port = 8000

def run_server(host, port):

    class User:

        def __init__(self, transport, peername):
            self.user_transport = transport
            self.user_peername = peername
            self.count = 0

    class Node:

        def __init__(self, transport, peername):
            self.user_transport = transport
            self.user_peername = peername
            self.count = 0

    class ClientServerProtocol(asyncio.Protocol):

        active_users = []
        active_nodes = []

        selfadress = (host,port)

        def connection_made(self, transport):
            self.peername = transport.get_extra_info('peername')
            print('New connection from {}'.format(self.peername))
            self.transport = transport
            self.data = b""

            user = User(self.transport, self.peername)
            self.active_users.append(user)

            name = "/node " + host + " " + str(port) + "\n"
            self.transport.write(name.encode())

        def connection_lost(self, exc):
            str = "left our group \n"
            self.process_data(str)

            for user in self.active_users:
                if user.user_transport == self.transport:
                    self.active_users.remove(user)
                    print('Close connection from {}'.format(user.user_name))

        def data_received(self, data):
            if self.data:
                data = self.data + data
                self.data = b""
            self.process_data(data.decode('utf-8'))

        def process_data(self, data):
            perenos = data[len(data)-1:len(data)]
            if perenos == "\r" or perenos == "\n":
                data = data[:len(data)-1]
            perenos = data[len(data) - 1:len(data)]
            if perenos == "\r" or perenos == "\n":
                data = data[:len(data) - 1]

            print(data)
            if data == "/node":
                for user in self.active_users:
                    if user.user_transport == self.transport:
                        self.active_users.remove(user)
                        self.active_nodes.append(user)

            if data == "/print":
                self.printAllUsers()

            if data == "/self":
                self.printSelfAdress()

            if data.__contains__("/connect"):
                split = data.split(" ")
                self.connectTo(split[1], split[2])

            if data.__contains__("/node"):
                split = data.split(" ")
                for user in self.active_users:
                    if user.user_transport == self.transport:
                        self.active_users.remove(user)
                        newNode = Node(user.user_transport,user.user_peername)
                        self.active_nodes.append(newNode)

            for user in self.active_users:
                if user.user_transport != self.transport:
                    str = "[{}]: ".format(user.user_peername) + data + "\n"
                    user.user_transport.write(str.encode())
                else:
                    str = ">>"


        def printAllUsers(self):
            str = "\n"
            str = str + "Users: \n"
            for user in self.active_users:
                str = str + "{}".format(user.user_peername) + "\n"
            str = str + "Nodes: \n"
            for user in self.active_nodes:
                str = str + "{}".format(user.user_peername) + "\n"
            str = str + "\n"
            self.transport.write(str.encode())

        def printSelfAdress(self):
            adress = "node " + self.selfadress[0] + ":" + str(self.selfadress[1]) + "\n\n"
            self.transport.write(adress.encode())

        def connectTo(self, host, port):
            print(host+port)

            loop = asyncio.get_event_loop()
            coro = loop.create_connection(ClientServerProtocol, host, int(port))
            loop.run_until_complete(coro)
            loop.run_forever()
            loop.close()


    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


run_server(IP, Port)
