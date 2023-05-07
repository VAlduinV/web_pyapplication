import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import json
from datetime import datetime
import threading
import socket


# HTTP сервер
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Розділяємо шлях запиту та отримуємо шлях і параметри
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            # Головна сторінка - index.html
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif path == '/message':
            # Сторінка з формою - message.html
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('message.html', 'rb') as file:
                self.wfile.write(file.read())
        elif path == '/style.css':
            # Статичний файл - style.css
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('style.css', 'rb') as file:
                self.wfile.write(file.read())
        elif path == '/logo.png':
            # Статичний файл - logo.png
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('logo.png', 'rb') as file:
                self.wfile.write(file.read())
        else:
            # Сторінка 404 Not Found
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('error.html', 'rb') as file:
                self.wfile.write(file.read())

    def do_POST(self):
        # Обробка POST-запиту
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(post_data)

        if self.path == '/message':
            # Отримання даних з форми
            username = params['username'][0]
            message = params['message'][0]

            # Відправка даних до Socket серверу
            send_to_socket_server(username, message)

            # Перенаправлення на головну сторінку після відправки повідомлення
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()


# Функція для відправки даних до Socket
def send_to_socket_server(username, message):
    data = {
            'username': username,
            'message': message
           }
    json_data = json.dumps(data).encode('utf-8')
    # Встановлення з'єднання з Socket сервером
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)

    try:
        # Відправка даних на Socket сервер
        client_socket.sendto(json_data, server_address)
    finally:
        # Закриття з'єднання
        client_socket.close()


def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5000)
    server_socket.bind(server_address)
    while True:
        # Отримання даних від веб-програми
        data, address = server_socket.recvfrom(4096)
        json_data = data.decode('utf-8')
        message_data = json.loads(json_data)

        # Збереження даних у файл data.json
        with open('storage/data.json', 'a') as file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            message = {
                timestamp: message_data
            }
            file.write(json.dumps(message) + '\n')


if __name__ == '__main__':
    print('''
            _   _ _____ ___________                                    
            | | | |_   _|_   _| ___ \                                   
            | |_| | | |   | | | |_/ /_____ ___  ___ _ ____   _____ _ __ 
            |  _  | | |   | | |  __/______/ __|/ _ \ '__\ \ / / _ \ '__|
            | | | | | |   | | | |         \__ \  __/ |   \ V /  __/ |   
            \_| |_/ \_/   \_/ \_|         |___/\___|_|    \_/ \___|_|   
          ''')
    # Запуск HTTP сервера у окремому потоці
    http_thread = threading.Thread(target=lambda: http.server.HTTPServer(('localhost', 3000), MyHttpRequestHandler).serve_forever())
    http_thread.start()
    # Запуск Socket сервера у окремому потоці
    socket_thread = threading.Thread(target=socket_server)
    socket_thread.start()
