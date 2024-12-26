import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    with server_socket:
        client_socket, _ = server_socket.accept()
        request = client_socket.recv(4096)
        request_str = request.decode("utf-8")
        request_lines = request_str.split("\r\n")
        url_parts = request_lines[0].split(" ")
        # print(f"Request: {url_parts}")
        path = url_parts[1] if len(url_parts) > 1 else None
        
        if path and path != "/":
            client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")

        client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")


if __name__ == "__main__":
    main()
