import socket
import threading
import os
import time

print_lock = threading.Lock()
udp_port = 0

def main():
    global udp_port
    
    udp_port = int(input('Enter UDP port: '))
    path = 'list.txt'
    dis_interval = 5

    discovery_recv = threading.Thread(target=recv_nodes, args=(udp_port, path))
    discovery_recv.start()
    discovery_send = threading.Thread(target=send_nodes, args=(udp_port, path, dis_interval))
    discovery_send.start()


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

def recv_nodes(port, path):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.bind(('', port))
    print_clean('DISC RECV: Listening ...')
    while True:
        data, addr = sck.recvfrom(1024)
        data = data.decode('utf-8')
        cluster, port = extract_data(data)
        cluster.update({port: addr[0]})
        update_file(cluster, path)
        print_clean('DISC RECV: Discovery message received.')

def send_nodes(port, path, interval):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        cluster = read_file(path)
        data = build_message(cluster)
        for port, ip in cluster.items():
            sck.sendto(data.encode('utf-8'), (ip, port))
            print_clean('DISC SEND: Sent dis message to ' + ip + ':' + str(port))
        time.sleep(interval)

def print_clean(msg):
    print_lock.acquire()
    print(msg)
    print_lock.release()

if __name__ == "__main__":
    main()
