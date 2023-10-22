# Uncomment this to pass the first stage
import socket
import threading
import os
import sys
def parse_http_request(data):
    request_lines = data.split('\r\n')
    start_line = request_lines[0]
    
    method, path, protocol = start_line.split(' ')
    
    headers = {}
    
    for line in request_lines[1:]:
        if line.strip():
            key, value = line.split(': ', 1)
            headers[key] = value
    
    return method, path, protocol, headers
def handle_client(conn):
    data = conn.recv(1024).decode('utf-8')  # Receive and decode the request data
    if not data:
        return  # If no data is received, continue to the next iteration

    # Split the request into lines and get the first line (start line)

    # Extract the path from the start line
    method, path, protocol, headers = parse_http_request(data)
    # Check if the path is '/'
    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith('/files/'):
        filename = path[7:]
        directory = sys.argv[-1]
        file_path = os.path.join(directory, filename)
        print(directory)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_contents = file.read()
                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Type: application/octet-stream\r\n"
                response += f"Content-Length: {len(file_contents)}\r\n\r\n"
                response = response.encode() + file_contents
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
    elif path == '/user-agent':
        user_agent = headers.get('User-Agent', 'Unknown User-Agent')
        response = f"HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(user_agent)}\r\n\r\n"
        response += user_agent
        response.encode('utf-8')
    elif path.startswith('/echo/'):
        random_string = path[6:]  # Extract the random string
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(random_string)}\r\n\r\n"
        response += random_string
        response.encode('utf-8')
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        response.encode('utf-8')

    # Send the response back to the client
    conn.sendall(response)
    conn.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client,args=(conn,)).start()
        

if __name__ == "__main__":
    main()
