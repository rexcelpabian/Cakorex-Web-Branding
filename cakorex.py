import socket
import threading


def handle_connection(connectionSocket):
    message = connectionSocket.recv(1024).decode()
    print(message)
    
    # melakukan parsing request untuk klien
    request_method = message.split()[0]
    file_requested = message.split()[1]

    # file requestnya adalah indefix.html 
    if file_requested == '/':
        file_requested = '/indexfix.html'

    # penggunaan content type untuk mapping file extension
    content_types = {
        'png': 'image/png',
        'txt': 'text/plain',
        'jpeg': 'image/jpeg',
        'js': 'application/javascript',
        'video': 'video/mp4',
        'scss': 'text/css',
        'html': 'text/html',
        'css': 'text/css',
        'jpg': 'image/jpeg',
    }

    # parsing (membuka file requestan client)
    try:
        file_extension = file_requested.split('.')[-1]
        with open(file_requested[1:], 'rb') as file:
            file_content = file.read()

        # pencarian content type sesuai file ekstensinya
        content_type = content_types.get(
            file_extension, 'application/octet-stream')

        # pencarian http response berdasarkan header dan file yang diperlukan
        response_header = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n'
        print(response_header)
        response_content = file_content

        # pengiriman http response ke client
        connectionSocket.send(response_header.encode())
        connectionSocket.send(response_content)

    # pengiriman pesan 404 not found
    except IOError as error:
        with open('404.html', 'rb') as file:
            file_content = file.read()

        response_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'
        response_content = file_content
        print(error)

        # pengiriman pesan 404 not found
        connectionSocket.send(response_header.encode())
        connectionSocket.send(response_content)
    # tutup koneksi soket
    connectionSocket.close()


# buat TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# aktivasi SO_REUSEADDR
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# aktivasi SO_KEEPALIVE
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# menghubungkan soket ke lokalhost dan port 80
serverHost = 'localhost'  # alamat IP lokal
serverPort = 80  # port yang digunakan

# menggabungkan host dan port (binding)
serverSocket.bind((serverHost, serverPort))

# digunakan untuk menerima koneksi dari client
serverSocket.listen(1)

print(f'Klik disini http://{serverHost}:{serverPort}/')
while True:
    # digunakan untuk nerima koneksi klien
    connectionSocket, addr = serverSocket.accept()

    # buat thread baru
    t = threading.Thread(target=handle_connection, args=(connectionSocket,))
    t.start()
