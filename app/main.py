import socket  # noqa: F401
from concurrent.futures import ThreadPoolExecutor
import argparse

def main(*args, **kwargs):
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, help='Optional directory argument', required=False)
    args = parser.parse_args()

    dir_path = args.directory
    print(f"Directory: {dir_path}")

    def handle_client_connection(client_socket, dir_path):
        print("Handling client connection")
        try:
            with client_socket:
                request = client_socket.recv(4096)
                print(f"Request: {request}")

                request_str = request.decode("utf-8")
                request_lines = request_str.split("\r\n")
                url_parts = request_lines[0].split(" ")

                print(f"Request: {url_parts}")
                path = url_parts[1] if len(url_parts) > 1 else None

                if not path:
                    client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

                
                if path == "/":
                    print("Root path")
                    client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
                
                elif path.lower().startswith("/file"):
                    file_name = path[7:]
                    print(f"File path: {dir_path} {file_name}")
                    import os
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        with open(file_path, "rb") as file:
                            file_content = file.read()
                            respond_text = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(file_content)}\r\n\r\n{file_content.decode('utf-8')}\r\n\r\n"
                            client_socket.sendall(respond_text.encode("utf-8"))
                    except FileNotFoundError:
                        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
                
                elif path.lower().startswith("/echo"):
                    message = path[6:]
                    respond_text = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(message)}\r\n\r\n{message}\r\n"
                    client_socket.sendall(respond_text.encode("utf-8"))

                elif path.lower().startswith("/user-agent"):
                    header = None
                    for req_line in request_lines:
                        if req_line and  req_line.startswith("User-Agent:"):
                            header = req_line
                            break
                    
                    if not header:
                        client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
                        return

                    message = header.split("User-Agent: ")[1]
                    respond_text = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(message)}\r\n\r\n{message}\r\n"
                    client_socket.sendall(respond_text.encode("utf-8"))
                else:
                    client_socket.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
        except BrokenPipeError:
            print("Client closed connection")
        except Exception as e:
            print(f"Error: {e}")
            client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")

    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    with ThreadPoolExecutor(max_workers=10) as executor:
        with server_socket:
            while True:
                print("Server started")
                client_socket, _ = server_socket.accept()
                print("Client connected")
                executor.submit(handle_client_connection, client_socket, dir_path)


            

if __name__ == "__main__":
    main()
