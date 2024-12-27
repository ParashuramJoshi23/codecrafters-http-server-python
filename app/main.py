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

        print(f"Request: {request_lines}")

        if not path:
            client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")

        
        if path == "/":
            print("Root path")
            client_socket.send(b"HTTP/1.1 200 OK\r\n\r\n")
        
        elif path.lower().startswith("/echo"):
            message = path[6:]
            respond_text = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(message)}\r\n\r\n{message}\r\n"
            client_socket.send(respond_text.encode("utf-8"))

        elif path.lower().startswith("/user-agent"):
            header = None
            for req_line in request_lines:
                if req_line and  req_line.startswith("User-Agent:"):
                    header = req_line
                    break
            
            if not header:
                client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
                return

            message = header.split("User-Agent: ")[1]
            respond_text = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(message)}\r\n\r\n{message}\r\n"
            client_socket.send(respond_text.encode("utf-8"))


        
        else:
            client_socket.send(b"HTTP/1.1 404 Not Found\r\n\r\n")


            

if __name__ == "__main__":
    main()
