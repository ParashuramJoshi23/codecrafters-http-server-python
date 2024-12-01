# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=False)
    server_socket.listen(1)
    print("Server started!")

    while True:
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        start_line, header1, header2 = request.partition(b"\r\n")
        print(f"Received: {start_line} header 1: {header1} header 2: {header2}")
        print(f"Connection from {addr}")

        start_line_data = start_line.split(b" ")
        method = start_line_data[0]
        url = start_line_data[1].decode("utf-8")
        proto = start_line_data[2]
        print(f"Method: {method} URL: {url} Protocol: {proto}")

        if url == "/":
            content = ""
            print(f"Content: {content}")
            client_socket.sendall(b"""HTTP/1.1 200 OK\r\n\r\n""")
            client_socket.close()
        elif url.startswith("/echo/"):
            content = url.split("/echo/")[1]
            result = f"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}"""
            client_socket.sendall(result.encode("utf-8"))
            client_socket.close()
        else:
            client_socket.sendall(b"""HTTP/1.1 404 NOT FOUND\r\n\r\n""")
            client_socket.close()

if __name__ == "__main__":
    main()
