#! /Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import random
import threading

ipandport = "Someone"

bannedip = []

def advert():
    adverts = []
    with open("adverts.txt") as f:
        adverts = f.readlines()
        f.close()
    
    threading.Timer(138.0, advert).start()
    msg = adverts[random.randint(0,((len(adverts)-1)))]
    message = (msg+"~Advert").encode("utf8")
    prefix = ("Advert: ")
    broadcast(message, prefix)


def refreshban():
    global bannedip
    fh = open("banned.txt")
    bannedip = fh.readlines() 
    fh.close()

def ban(ip):
    fh = open("banned.txt", 'a')
    fh.write(ip+"\n")
    fh.close()
    print("Banned "+ip)
    refreshban()
    kick(ip)

    
def kick(ip):
    global members
    try:
        client = members[ip]
        client.send(bytes("{quit}", "utf8"))
        client.close()
        del clients[client]
        broadcast(bytes("Someone has been kicked.~Host", "utf8"))
        return 1
    except KeyError:
        return 0
    
refreshban()    

def accept_incoming_connections():
    global ipandport
    global bannedip
    while True:
        client, client_address = SERVER.accept()
        addr = ("%s:%s" % client_address)
        ipandport = addr.split(":")
        if ipandport[0] in bannedip:
            print("a banned person tried to enter")
        else:
            client.send(bytes("Type your name and press enter!~Host", "utf8"))
            addresses[client] = client_address
            members[ipandport[0]] = client
            Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    global ipandport
    global clients
    global addresses
    name = client.recv(BUFSIZ).decode("utf8")

    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.~Host' % name
    if name == "_advert_":
        print("allowed")
    else:
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!~Host" % name
        print(ipandport[0]+" has connected with the alias: "+name)
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
        
    while True:
        msg = client.recv(BUFSIZ)
        raw_message = (msg.decode('utf8'))

        

        addr = ("%s:%s" % addresses[client])
        ipandport = addr.split(":")
        
        msg = (raw_message+"~"+ipandport[0]).encode("utf8")
        print(msg.decode("utf8"))
        if raw_message.startswith("vMXHZJKCI3OtcSZo:"):
            raw_ip = raw_message.split(":")
            ban(raw_ip[1])

        elif raw_message.startswith("jhsJHGSuyaysabJKH:"):
            raw_ip = raw_message.split(":")
            kicked = kick(raw_ip[1])
            if kicked == 0:
                client.send(bytes("IP not Found: "+raw_ip[1]+"~Host", "utf8"))
            else:
                client.send(bytes(("Kicked "+raw_ip[1]+"~Host"), "utf8"))

        elif raw_message.startswith("sandkKHKUsbjsaJHBHJ:"):
            f = open("bannedip.txt", "w")
            f.close()

        elif raw_message.startswith("kjahdskKJGhsvaj:"):
            raw_shout = raw_message.split(":")
            shout = (raw_shout[1]+"~Announcement").encode("utf8")
            print("Announcement: "+shout.decode("utf8"))
            broadcast(shout, "Announcement: ")
        else:
            if msg != bytes("{quit}", "utf8"):
                message = bytes((raw_message+"~"+ipandport[0]).encode("utf8"))
                broadcast(msg, name+": ")
            else:
                client.close()
                del clients[client]
                broadcast(bytes(name+" has left the chat~Host", "utf8"))
                break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf8")+msg)
        except BrokenPipeError:
            print("Broken Pipe Error")

        
clients = {}
addresses = {}
members = {}

#HOST = 'chat.derailerofficial.co.uk'
HOST = '192.168.0.50'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)


SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
advert()
if __name__ == "__main__":
    SERVER.listen(5)
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
