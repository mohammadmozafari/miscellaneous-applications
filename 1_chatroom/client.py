import json
import requests
from threading import Thread

join_path = 'http://localhost:8080/join'
get_path = 'http://localhost:8080/get'
send_path = 'http://localhost:8080/send'
token = None
uname = None

def main():
    enter()
    Thread(target=get_message, args=()).start()
    send_message()

def enter():
    global token, uname
    while True:
        uname = input('Enter your username: ')
        resp = requests.post(join_path, data=json.dumps({'username':uname}))
        if resp.status_code != 200:
            print('Username is not accepted. Try again!')
        else:
            print('Welcome to chatroom')
            token = resp.json()['token']
            print('My token:', token)
            print('------------------------------------\n')
            break

def get_message():
    while True:
        resp = requests.get(get_path, headers={'Sender': token})
        if resp.status_code == 200:
            dic = resp.json()
            sender = dic['sender']
            message = dic['message']
            if sender != uname:
                print('{}: {}'.format(sender, message))

def send_message():
    while True:
        message = input()
        requests.post(send_path, headers={'Sender': token}, data=json.dumps({'message':message}))

if __name__ == "__main__":
    main()
