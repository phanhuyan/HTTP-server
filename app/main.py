# Uncomment this to pass the first stage
import socket
MAX_CONNECTIONS = 10

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(MAX_CONNECTIONS)
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        response = "HTTP/1.1 200 OK\r\n\r\n"
        client_socket.send(response.encode())
        client_socket.close()

if __name__ == "__main__":
    main()
