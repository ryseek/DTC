import asyncio

#    reader, writer = asyncio.open_connection('192.168.31.253', 8888,

class MyEchoClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        message = "hello"
        transport.write(message.encode())
        print('Data sent: {!r}'.format(message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        loop.stop()


loop = asyncio.get_event_loop()
coro = loop.create_connection(MyEchoClientProtocol, '192.168.31.253', 8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()