import socket
import os
import threading
from datetime import datetime

IP = socket.gethostbyname(socket.gethostname())
PORT=4456
ADDR= (IP, PORT)
FORMAT = "utf-8"
CLIENT_DATA_PATH = "client_data"
SIZE = 100024
SEPARATOR = "<SEPARATOR>"
re=0
sent=0

def send_smallfile(fno,filename):
    if fno=="<<End>>":
        print("final Sent")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
        send_data=f"{fno}@{filename}@text"
        client.send(send_data.encode(FORMAT))
        data = client.recv(SIZE).decode(FORMAT)
        return

    with open(f"{CLIENT_DATA_PATH}/{filename}", "r") as f:
        text =f.read()
    send_data=f"{fno}@{filename}@{text}"    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    client.send(send_data.encode(FORMAT))
    data = client.recv(SIZE).decode(FORMAT)
    cmd, msg = data.split("@")
    if cmd!="OK":
        print(f"Unsuccessful{filename}")
    os.remove(f"{CLIENT_DATA_PATH}/{filename}")


def main():
    print("Enter path to file to be transfered")
    path=input("> ")
    lines_per_file = 300
    filename=path.split("/")[-1]
    smallfile =None
    count=0
    last=0
    re=0
    print("Transmission Started")
    print(datetime.now())
    with open(path) as bigfile:
        for lineno, line in enumerate(bigfile):
            last=lineno
            if lineno % lines_per_file ==0 :
                if smallfile:
                    smallfile.close()
                    global sent
                    sent=sent+1
                    thread = threading.Thread(target=send_smallfile, args=(count, small_filename))
                    thread.start()
                    count=count+1
                    #print(f"{lineno} and {small_filename}")

                small_filename= f"{lineno}-{filename}"
                smallfile= open(f"{CLIENT_DATA_PATH}/{small_filename}","w")
            smallfile.write(line)
        if smallfile:
            smallfile.close()
            #global sent
            sent=sent+1
            thread = threading.Thread(target=send_smallfile, args=(last, small_filename))
            thread.start()
    while threading.activeCount()>1:
        k=2
    thread=threading.Thread(target=send_smallfile, args=("<<End>>", filename))
    thread.start()

if __name__ == "__main__":
    main()