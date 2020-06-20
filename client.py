import socket
import threading
import os

DIS_PORT_SEND = 1441
DIS_PORT_RECV = 1440
DIS_FILE = 'cluster_nodes.txt'

def main():
    a = {'x': '11', 'y': '22'}
    print((serialize_dic(a)))
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
            f.write(y + ' ' + x + '\n')

def deserialize_string(st):
    st = st.strip()
    cluster = {}
    lines = st.split(' ')
    for line in lines:
        print(line)
        name, addr = line.split(',')
        cluster[addr] = name
    return cluster

def serialize_dic(dic):
    st = ''
    for x, y in dic.items():
        st += (y + ',' + x + ' ')
    return st.strip()

def recv_nodes():
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        data, addr = sck.recvfrom(1024)
        cluster = deserialize_string(data)
        update_cluster_file(cluster, DIS_FILE)
        print('discovery message recieved and merged.')

def send_nodes():
    while True:
        pass

if __name__ == "__main__":
    main()
