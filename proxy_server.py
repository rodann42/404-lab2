#!/usr/bin/env python3

import socket, sys

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip


def main():
    host = "www.google.com"
    port = 80

    #create start socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as start:
        print("Create proxy server")
        start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #q3, allows to reuse same bind port
        start.bind((HOST, PORT))
        start.listen(1) #make socket listen

        #listen forever for connections
        while True:
            conn, addr = start.accept() #accept incoming connections
            print("Connected by ", addr)
            #create end socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as end:
                print("Connecting to Google")
                # proxy_end.connect(sockaddr)
                remote_ip = get_remote_ip('www.google.com')

                end.connect((remote_ip , port))

                #receive the data from a client
                full_data = conn.recv(BUFFER_SIZE)
                print("Received data, now send it to google")
                #sending to google
                end.sendall(full_data)
                # when finish sending, shutdown
                end.shutdown(socket.SHUT_WR)

                # receive data back from google
                back_data = end.recv(BUFFER_SIZE)
                print("received data from google, send back to client")
                conn.send(back_data)

            conn.close()


if __name__ == "__main__":
    main()
