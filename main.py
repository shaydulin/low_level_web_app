import socket
import views


URLS = {
    "/": views.index,
    "/blog": views.blog,
}


def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 5000))
    server_socket.listen()

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request)
        print(addr)

        response = generate_response(request.decode())

        client_socket.sendall(response)
        client_socket.close()


def generate_response(request: str):
    method, url = request.split()[:2]
    headers, code = generate_headers(method, url)
    body = generate_body(code, url)
    return (headers + body).encode()


def generate_headers(method: str, url: str):
    if method != "GET":
        return "HTTP/1.1 405\n\n", 405
    if url not in URLS:
        return "HTTP/1.1 404\n\n", 404
    return "HTTP/1.1 200\n\n", 200


def generate_body(code: int, url: str):
    if code == 404:
        return "<h1>404</h1><p>Not Found</p>"
    if code == 405:
        return "<h1>405</h1><p>Method Not Allowed</p>"
    return URLS[url]()


if __name__ == "__main__":
    run()
