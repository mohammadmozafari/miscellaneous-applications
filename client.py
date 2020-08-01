import os
import time
import socket
import datetime
import threading
import random as rnd

udp_send_sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_recv_sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print_lock = threading.Lock()
udp_port = 0
tcp_port = 0
list_file = 'list.txt'
folder = './files'
disc_interval = 5
get_sent_time = None
download_wait = 2
current_request_file = None
response_buffer = []

def main():
    global udp_port, tcp_port, list_file, folder, download_wait, response_buffer, current_request_file
    
    udp_port = int(input('Enter UDP port: '))
    tcp_port = rnd.randint(12000, 13000)
    

    discovery_recv = threading.Thread(target=udp_recv, args=(udp_port, list_file))
    discovery_recv.start()
    discovery_send = threading.Thread(target=send_disc, args=(udp_port, list_file))
    discovery_send.start()

    while True:
        command = input()
        command = command.strip()
        
        if command == 'exit':
            return

        elif command[:3] == 'get':
            current_request_file = command[4:]
            udp_get(command[4:])
            time.sleep(download_wait)
            download_best()
            response_buffer = []
            current_request_file = None


def read_file(path):
    cluster = {}
    if not os.path.exists(path):
        return cluster
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            l = line.strip()
            port, ip = l.split(' ')
            cluster[int(port)] = ip
    return cluster

def update_file(new_cluster, path):
    cluster = read_file(path)
    cluster.update(new_cluster)
    st = ''
    with open(path, 'w') as f:
        for port, ip in cluster.items():
            if port == udp_port:
                continue
            st += str(port) + ' ' + ip + '\n'
        f.write(st.strip())

def extract_data(msg):
    msg = msg.strip()[5:]
    cluster = {}
    nodes = msg.split('\n')
    p = int(nodes[0])
    nodes = nodes[1:]
    for node in nodes:
        port, ip = node.split(' ')
        cluster[int(port)] = ip
    return cluster, p

def build_message(dic):
    st = 'Disc {}\n'.format(udp_port)
    for port, ip in dic.items():
        st += '{} {}\n'.format(port, ip)
    return st.strip()

def send_disc(port, path):
    global udp_send_sck, disc_interval
    while True:
        cluster = read_file(path)
        data = build_message(cluster)
        for port, ip in cluster.items():
            udp_send_sck.sendto(data.encode('utf-8'), (ip, port))
            # print_clean('DISC SEND: Sent dis message to ' + ip + ':' + str(port))
        time.sleep(disc_interval)

def udp_recv(port, path):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.bind(('', port))
    print_clean('DISC RECV: Listening ...')
    while True:
        msg, addr = sck.recvfrom(1024)
        msg = msg.decode('utf-8')
        msg_type = msg[:4]
        
        if msg_type == 'Disc':
            cluster, port = extract_data(msg)
            cluster.update({port: addr[0]})
            update_file(cluster, path)

        elif msg_type == 'Gett':
            process_get(msg, addr)

        elif msg_type == 'Resp':
            process_resp(msg, addr)

        else:
            print_clean('Message format not supported.')

def udp_get(filename):
    global list_file, udp_send_sck, udp_port
    nodes = read_file(list_file)
    msg = 'Gett {} {}'.format(filename, udp_port)
    print_clean('\n----------------------------------')
    print_clean('Get message sent to:')
    for node in nodes.items():
        udp_send_sck.sendto(msg.encode('utf-8'), (node[1], node[0]))
        print_clean('   {}:{}'.format(node[1], node[0]))
    print()

def process_get(msg, source):
    global udp_send_sck, folder
    msg = msg.strip()[5:]
    filename, destination_port = msg.split(' ')
    destination_port = int(destination_port)
    if not os.path.exists(folder):
        return
    files = os.listdir(folder)
    for file in files:
        if file == filename:
            msg = build_get_response(filename)
            udp_send_sck.sendto(msg.encode('utf-8'), (source[0], destination_port))
            return

def process_resp(msg, source):
    global current_request_file
    msg = msg.strip()[5:]
    port, sent_time, filename = msg.split('\n')
    sent_time = datetime.datetime.strptime(sent_time, '%Y-%m-%d %H:%M:%S.%f')
    if filename == current_request_file:
        delay = datetime.datetime.now() - sent_time
        response_buffer.append((source[0], port, delay))

def build_get_response(filename):
    global tcp_port
    now = datetime.datetime.now()
    msg = 'Resp {}\n{}\n{}'.format(tcp_port, now, filename)
    return msg     

def download_best():
    global response_buffer
    if len(response_buffer) == 0:
        print('File wasn\'t found.')
    response_buffer.sort(key=lambda x:x[1])
    best = response_buffer[0]
    print(best)

def print_clean(msg):
    print_lock.acquire()
    print(msg)
    print_lock.release()

if __name__ == "__main__":
    # print(datetime.datetime.now())
    # t1 = datetime.datetime.now()
    # time.sleep(0.2)
    # t2 = datetime.datetime.now()

    # t0 = '2020-08-01 19:27:06.615044'

    # d = datetime.datetime.strptime(t0, '%Y-%m-%d %H:%M:%S.%f')

    # print(d)
    # print(t2 - d)
    # print(os.path.exists('x'))
    main()
