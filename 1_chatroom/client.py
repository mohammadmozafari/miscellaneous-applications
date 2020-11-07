import json
import requests
from threading import Thread

join_path = 'http://localhost:8080/join'
get_path = 'localhost:8080/get'
send_path = 'localhost:8080/send'

def main():
    enter()
    listener = Thread()

def enter():
    while True:
        uname = input('Enter your username: ')

        resp = requests.post(join_path, data=json.dumps({'username':uname}))
        print('shit')
        if resp.status_code != 200:
            print('Username is not accepted. Try again!')
        else:
            print('Welcome to chatroom')
            token = resp.json()['token']
            print('My token:', token)
            break

if __name__ == "__main__":
    main()
