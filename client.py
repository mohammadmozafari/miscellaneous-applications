import socket
import threading
import os
import time

print_lock = threading.Lock()

def main():
    dis_listen_port = 1446
    dis_file_path = 'list.nw'
    dis_interval = 5

    discovery_recv = threading.Thread(target=recv_nodes, args=(dis_listen_port, dis_file_path))
    discovery_recv.start()

    discovery_send = threading.Thread(target=send_nodes, args=(dis_listen_port, dis_file_path, dis_interval))
    discovery_send.start()

def read_cluster_file(path):
    cluster = {}
    if not os.path.exists(path):
        return cluster
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            l = line.strip()
            name, addr = l.split(' ')
            cluster[name] = addr
    return cluster

def update_cluster_file(new_cluster, path):
    cluster = read_cluster_file(path)
    cluster.update(new_cluster)
    with open(path, 'w') as f:
        for x, y in cluster.items():
            if x == socket.gethostname():
                continue
            f.write(x + ' ' + y + '\n')

def deserialize_string(st):
    st = st.strip()
    cluster = {}
    nodes = st.split(' ')
    for node in nodes:
        name, addr = node.split(',')
        cluster[name] = addr
    return cluster

def serialize_dic(dic):
    st = ''
    for x, y in dic.items():
        st += (x + ',' + y + ' ')
    return st.strip()

def recv_nodes(port, path):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.bind(('', port))
    print_clean('DISC RECV: Listening ...')
    while True:
        data, addr = sck.recvfrom(1024)
        data = data.decode('utf-8')
        cluster = deserialize_string(data)
        cluster.update({socket.gethostbyaddr(addr[0])[0]: addr[0]})
        update_cluster_file(cluster, path)
        print_clean('DISC RECV: Discovery message received.')

def send_nodes(port, path, interval):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        cluster = read_cluster_file(path)
        data = serialize_dic(cluster)
        for name, addr in cluster.items():
            sck.sendto(data.encode('utf-8'), (addr, port))
            print_clean('DISC SEND: Sent dis message to ' + addr)
        time.sleep(interval)

def print_clean(msg):
    print_lock.acquire()
    print(msg)
    print_lock.release()

if __name__ == "__main__":
    main()
