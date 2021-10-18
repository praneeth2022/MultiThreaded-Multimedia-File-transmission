
import os,glob
import socket
import threading
from datetime import datetime

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 100024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"
SEPARATOR = "<SEPARATOR>"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    #conn.send("OK@Welcome to the File Server.".encode(FORMAT))
    data = conn.recv(SIZE).decode(FORMAT)
    data = data.split("@")
    cmd = data[0]
    if cmd == "<<End>>":
        filename=data[1]
        print(filename)
        #os.chdir(SERVER_DATA_PATH)
        #read_files =glob.glob("{SERVER_DATA_PATH}/*{filename}")
        with open(filename, "wb") as outfile:
            for f in os.listdir(SERVER_DATA_PATH):
                if f.endswith(filename):
                    #print(f)
                    with open(f"{SERVER_DATA_PATH}/{f}", "rb") as infile:
                        outfile.write(infile.read())
                    os.remove(f"{SERVER_DATA_PATH}/{f}")
        print("Transmission Completed")
        print(datetime.now())
        send_data2 = "OK@File uploaded successfully."
        conn.send(send_data2.encode(FORMAT))
        conn.close()
        return


    name,text=data[1],data[2]
    filepath =os.path.join(SERVER_DATA_PATH,name)
    with open(filepath,"w") as f:
        f.write(text)
    #print(f"Received {name}")
    send_data = "OK@File uploaded successfully."
    conn.send(send_data.encode(FORMAT))

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def main():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
if __name__ == "__main__":
    main()
