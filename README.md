# DTC
Decentralized TCP Chat in pure **Python**.

Basically it's just small step into blockchain world.
It was coded using Python's asyncio and protocol factories.
This code creates server, that listens to TCP connections.
Anyone can connect to this server (for example using _telnet_).
Everything, that was uploaded over that connection will push to other active connections.
Also this server can connect to another server.
This way it is possible to create a decentralized network using almost identical code for each node.

# Setup guide

Requirements: **Python 3.4** and above.

Add IP and port that opened in this lines in file `node.py`: 
```
IP = "127.0.0.1"
Port = 8000
```
And run this python file. 

# How to test it

We can create a special client app, but it's easier to use **telnet**.
Run in terminal:
```
telnet 127.0.0.1 8000
```
It opens a TCP connection to server. 
If you will write something there and hit `Enter` button server will receive this message and send it to other connected users.
So to see it run the same command in new terminal window. 

# Prompt Commands

This commands are used to control the server from TCP connection

`/print` - prints all the users and nodes, connected to this server/node

`/self` - prints IP and Port of this exact node/server

`/connect <ip> <port>` - create connection from this node to other node