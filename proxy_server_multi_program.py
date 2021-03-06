import socket, sys
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024
def get_remote_ip(host):
    print(f'Getting IP  for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip


def handle_request(conn, addr, proxy_end):
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending received data {send_full_data} to google")
    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)

    data = proxy_end.recv(BUFFER_SIZE)
    print(f'Sending received data {data} to client')
    conn.send(data)


def main():
    host = 'www.google.com'
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
                remote_ip = get_remote_ip('www.google.com')

                end.connect((remote_ip , port))

                # handle multiple request
                p = Process(target=handle_request, args=(conn, addr, proxy_end))
                p.daemon = True
                p.start()
                print("Started process ", p)

            conn.close()


if __name__ == "__main__":
    main()
