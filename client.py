import socket
import threading
import os

DIS_PORT_SEND = 1441
DIS_PORT_RECV = 1440
DIS_FILE = 'cluster_nodes.txt'

def main():
    print(read_cluster_file(DIS_FILE))
    c = {'11':'a', '22':'d'}
    update_cluster_file(c, DIS_FILE)
    print(read_cluster_file(DIS_FILE))
    # discovery_recv = threading.Thread(target=recv_nodes, args=(DIS_PORT_RECV, DIS_FILE))
    # discovery_send = threading.Thread(target=send_nodes, args=(DIS_PORT_SEND, DIS_FILE))


def read_cluster_file(file):
    cluster = {}
    if not os.path.exists(file):
        return None
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            addr, name = line.split(' ')
            name = name[:-1]
            cluster[addr] = name
    return cluster

def update_cluster_file(new_cluster, file):
    if os.path.exists(file):
        cluster = read_cluster_file(file)
        cluster.update(new_cluster)
    else:
        cluster = new_cluster
    with open(file, 'w') as f:
        for x, y in cluster.items():
            f.write(x + ' ' + y + '\n')

def recv_nodes():
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        data, addr = sck.recvfrom(1024)
        print('discovery message recieved.')

def send_nodes():
    while True:
        pass

if __name__ == "__main__":
    main()
