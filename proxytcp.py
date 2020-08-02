import socket
import threading
import os.path


def proxytoserver():
    while True:
        data = conn.recv(2048)
        server_socket.send(data)
        print("[" + str(address) + " Data1]: " + str(data))


def servertoproxy():
    while True:
        data2 = server_socket.recv(2048)
        print("[" + str(address) + " Data2]: " + str(data2))
        conn.send(data2)


def save_to_file():
    # init the file
    f = 0

    # checking if the file exists, if not create it
    if os.path.exists('./save.txt'):
        # opening existing file
        f = open("save.txt", "a")
    else:
        # opening new file
        f = open("save.txt", "x")

    # write/append to file and closing the writer
    f.write(proxy_server_address + "," + proxy_server_port + "," + server_address + "," + server_port)
    f.close()


def read_from_file():
    f = 0

    if os.path.exists('./save.txt'):
        f = open("save.txt")
    else:
        print("there were no saved values found")
        exit()


use_saved = input("do you want to use your saved values? (y/n)")
if use_saved == "y":

    read_from_file()

else:

    proxy_server_address = input("please set your proxy address: ")
    proxy_server_port = input("please set your proxy port: ")
    server_address = input("please set your server address: ")
    server_port = input("please set your server port: ")
    save_inputs = input("would you like to save your inputs for next time? (y/n): ")

    if save_inputs == "y":
        save_to_file()

    try:
        # create the server socket
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the server socket to its IP and Port
        proxy_socket.bind((proxy_server_address, int(proxy_server_port)))

        # make the server listen
        proxy_socket.listen(5)
    except:
        print("could not create proxy at " + proxy_server_address + ":" + proxy_server_port)
        exit()
    else:

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((server_address, int(server_port)))
        except:
            print("could not connect to Server at " + server_address + ":" + server_port)
            exit()
        else:
            print("listening on proxy " + proxy_server_address + ":" + proxy_server_port)
            print("")
            conn, address = proxy_socket.accept()
            thread1 = threading.Thread(target=proxytoserver)
            thread1.start()

            thread2 = threading.Thread(target=servertoproxy)
            thread2.start()
