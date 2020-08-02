import os.path
import socket


# method to save log message to a file
def savefile(message):
    # init the file
    f = 0

    # checking if the file exists, if not create it
    if (os.path.exists('./log.txt')):
        # opening existing file
        f = open("log.txt", "a")
    else:

        print("log file does not exist")
        print("creating...")

        # opening new file
        f = open("log.txt", "x")

    # write/append to file and closing the writer
    f.write(message)
    f.close()


def createserver():
    print("please specify your protocol: <tcp/udp/end>")
    protocol = input("")

    if protocol == "tcp":

        server_address = input("please set your address: ")
        server_port = input("please set your port: ")

        try:
            # create the server socket
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # bind the server socket to its IP and Port
            serversocket.bind((server_address, int(server_port)))
            # make the server listen
            serversocket.listen()
        except:
            print("could not create server on " + server_address + ":" + server_port)
            exit()
        else:
            print("listening to " + server_address + ":" + server_port)

        # server loop
        while True:
            # accepts incoming connection
            conn, address = serversocket.accept()

            # prints the address and port the connection was accepted from

            # receives data
            data = conn.recv(1024)

            # prints data to console and log file
            print("[" + str(address) + "]: " + str(data))
            savefile("[Client]: " + str(data))

            if (str(data)).__contains__("end"):
                del data
            elif (str(data)).__contains__("answer me"):
                conn.send(("answer").encode('utf-8'))
                del data

    elif protocol == "udp":

        server_address = input("please set your address: ")
        server_port = input("please set your port: ")

        try:
            serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            serversocket.bind((server_address, int(server_port)))
        except:
            print("could not create server on " + server_address + ":" + server_port)
            exit()
        else:
            print("listening to " + server_address + ":" + server_port)

        while True:

            # receives data
            data, address = serversocket.recvfrom(1024)
            print("got connection from", address)

            # prints data to console and log file
            print("[Client]: " + str(data))
            savefile("[Client]: " + str(data))

            if (str(data)).__contains__("end"):
                del data
            elif (str(data)).__contains__("answer me"):
                serversocket.sendto(b"test", address)
                del data

    elif protocol == "end":
        print("ending script")
        exit()
    else:
        temp = input(protocol + " was no option. do you want to exit? (y/n): ")

        if temp == "n":
            createserver()
        else:
            print("exiting")
            exit()


createserver()