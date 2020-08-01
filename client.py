import socket
import threading
import os
import time
import datetime

print_lock = threading.Lock()
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_port = 0
tcp_port = 0
list_file = 'list.txt'
folder = 'files'

def main():
    global udp_port, list_file, folder
    
    udp_port = int(input('Enter UDP port: '))
    dis_interval = 5

    discovery_recv = threading.Thread(target=udp_recv, args=(udp_port, list_file))
    discovery_recv.start()
    discovery_send = threading.Thread(target=send_nodes, args=(udp_port, list_file, dis_interval))
    discovery_send.start()

    while True:
        command = input()
        
        
        if command == 'exit':
            return


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

def send_nodes(port, path, interval):
    global send_socket
    while True:
        cluster = read_file(path)
        data = build_message(cluster)
        for port, ip in cluster.items():
            send_socket.sendto(data.encode('utf-8'), (ip, port))
            # print_clean('DISC SEND: Sent dis message to ' + ip + ':' + str(port))
        time.sleep(interval)

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
            pass
        else:
            print_clean('Message format not supported.')

def process_get(msg, source):
    global send_socket
    msg = msg.strip()[5:]
    filename, destination_port = msg.split(' ')
    destination_port = int(destination_port)
    files = os.listdir('./path')
    for file in files:
        if file == filename:
            msg = build_get_response(filename)
            send_socket.sendto(msg.encode('utf-8'), (source[0], destination_port))
            return

def build_get_response(filename):
    global tcp_port
    now = datetime.datetime.now()
    msg = 'Resp {}\n{}'.format(tcp_port, now)
    return msg            

def print_clean(msg):
    print_lock.acquire()
    print(msg)
    print_lock.release()

if __name__ == "__main__":
    # print(datetime.datetime.now())
    t1 = datetime.datetime.now()
    time.sleep(0.2)
    t2 = datetime.datetime.now()

    t0 = '2020-08-01 19:27:06.615044'

    d = datetime.datetime.strptime(t0, '%Y-%m-%d %H:%M:%S.%f')

    print(d)
    print(t2 - d)
    # main()
