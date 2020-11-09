import os
import sys
import time
import socket
import datetime
import threading
import random as rnd

current_request_file = None
response_buffer = []
num_tcp_connections = 0
prior_communications = {}

def main(params):
    global response_buffer, current_request_file
    
    hname = params[0]
    udp_port = int(params[1])
    list_file = params[2]
    folder = params[3]
    interval = float(params[4])
    wait = float(params[5])
    connection_limit = int(params[6])
    tcp_port = get_random_port()
    if not folder.endswith('/'):
        folder += '/'

    print('UDP listening on {}'.format(udp_port))
    print('TCP listening on {}'.format(tcp_port))
    
    tcp_receiver = threading.Thread(target=tcp_recv,
                                    args=(tcp_port, folder))
    tcp_receiver.start()
                                    
    udp_receiver = threading.Thread(target=udp_recv,
                                    args=(udp_port, list_file, folder,
                                          tcp_port, connection_limit, hname))
    udp_receiver.start()
                                          
    udp_sender = threading.Thread(target=udp_send_discovery,
                                  args=(udp_port, list_file, interval, hname))
    udp_sender.start()

    while True:
        print('\n----------------------------------')
        command = input('> ')
        command = command.strip()
        
        if command == 'exit':
            os._exit(0)

        elif command == 'list':
            print()
            display_list(list_file)

        elif command[:3] == 'get':
            filename = command[4:]
            current_request_file = filename
            udp_send_gett(filename, list_file, udp_port, hname)
            time.sleep(wait)
            best = find_best_candidate()
            if best == None:
                continue
            response_buffer = []
            current_request_file = None
            download_from(filename, best, folder)
        
        else:
            print('Command not found.')
            pass

# ---------------------------------------------------------------
# These functions help build dictionaries from list files and
# discovery messages and encoding dictionaries
# for transmitting them.
# ---------------------------------------------------------------

def read_file(path):
    cluster = {}
    if not os.path.exists(path):
        return cluster
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            l = line.strip()
            name, ip, port = l.split(' ')
            cluster[name] = (ip, int(port))
    return cluster

def update_file(new_cluster, path, hname):
    cluster = read_file(path)
    cluster.update(new_cluster)
    st = ''
    with open(path, 'w') as f:
        for name, (ip, port) in cluster.items():
            if name == hname:
                continue
            st += '{} {} {}\n'.format(name, ip, port)
        f.write(st)

def extract_data(msg):
    msg = msg.strip()[5:]
    cluster = {}
    nodes = msg.split('\n')
    n, p = nodes[0].split(' ')
    p = int(p)
    nodes = nodes[1:]
    for node in nodes:
        name, ip, port = node.split(' ')
        cluster[name] = (ip, port)
    return cluster, n, p

def build_message(dic, udp_port, node_name):
    st = 'Disc {} {}\n'.format(node_name, udp_port)
    for name, (ip, port) in dic.items():
        st += '{} {} {}\n'.format(name, ip, port)
    return st


# ---------------------------------------------------------------
# These functions are used for sending, receiving
# and processing different udp and tcp requests.
# ---------------------------------------------------------------

def tcp_recv(tcp_port, folder):
    global num_tcp_connections
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.bind(('', tcp_port))
    sck.listen(20)
    while True:
        connection, addr = sck.accept()
        num_tcp_connections += 1
        filename = connection.recv(1024).decode('utf-8')
        with open(folder + filename, 'rb') as f:
            l = f.read(1024)
            while l:
                connection.send(l)
                l = f.read(1024)
        connection.shutdown(socket.SHUT_WR)
        num_tcp_connections -= 1

def udp_recv(udp_port, path, folder, tcp_port, connection_limit, hname):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.bind(('', udp_port))
    while True:
        msg, addr = sck.recvfrom(1024)
        msg = msg.decode('utf-8')
        msg_type = msg[:4]
        
        if msg_type == 'Disc':
            cluster, name, port = extract_data(msg)
            # print(cluster, name, port)
            cluster.update({name: (addr[0], port)})
            update_file(cluster, path, hname)

        elif msg_type == 'Gett':
            if num_tcp_connections < connection_limit:
                udp_send_resp(msg, addr, folder, tcp_port, hname)

        elif msg_type == 'Resp':
            save_resp(msg, addr)

        else:
            print('Message format not supported.')

def udp_send_discovery(udp_port, path, interval, node_name):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        cluster = read_file(path)
        data = build_message(cluster, udp_port, node_name)
        for name, (ip, port) in cluster.items():
            sck.sendto(data.encode('utf-8'), (ip, port))
        time.sleep(interval)

def udp_send_gett(filename, list_file, udp_port, hname):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    nodes = read_file(list_file)
    msg = 'Gett {}\n{} {}'.format(filename, hname, udp_port)
    print('\nGet message sent to:')
    for name, (ip, port) in nodes.items():
        sck.sendto(msg.encode('utf-8'), (ip, port))
        print('   {} - {}:{}'.format(name, ip, port))
    print()

def udp_send_resp(msg, source, folder, tcp_port, hname):
    global prior_communications
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = msg.strip()[5:]
    filename, destination = msg.split('\n')
    dname, dport = destination.split(' ')
    dport = int(dport)
    count = prior_communications.get(dname, 0)
    delay = 1.0 / (2 ** count)
    if not os.path.exists(folder):
        return
    files = os.listdir(folder)
    for file in files:
        if file == filename:
            msg = build_get_response(filename, hname, tcp_port)
            time.sleep(delay)
            sck.sendto(msg.encode('utf-8'), (source[0], dport))
            return

def save_resp(msg, source):
    global current_request_file, response_buffer
    msg = msg.strip()[5:]
    destination, sent_time, filename = msg.split('\n')
    dname, dport = destination.split(' ') 
    dport = int(dport)
    sent_time = datetime.datetime.strptime(sent_time, '%Y-%m-%d %H:%M:%S.%f')
    if filename == current_request_file:
        delay = (datetime.datetime.now() - sent_time).total_seconds()
        response_buffer.append((dname, source[0], dport, delay))


def build_get_response(filename, hname, tcp_port):
    now = datetime.datetime.now()
    msg = 'Resp {} {}\n{}\n{}'.format(hname, tcp_port, now, filename)
    return msg     

def find_best_candidate():
    global response_buffer
    if len(response_buffer) == 0:
        print('File wasn\'t found.')
        return None
    print('File was found on:')
    for res in response_buffer:
        print('  {} - {}:{} with delay {} seconds'.format(res[0], res[1], res[2], res[3]))
    response_buffer.sort(key=lambda x:x[3])
    best = response_buffer[0]
    print('\nDownloading from {} - {}:{} ...'.format(best[0], best[1], best[2]))
    return best

def download_from(filename, host, folder):
    global prior_communications
    buff = 1024
    hname, ip, port = host[0], host[1], host[2]
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.connect((ip, port))
    sck.send(filename.encode('utf-8'))
    with open(folder + filename, 'wb') as f:
        l = sck.recv(buff)
        while l:
            f.write(l)
            l = sck.recv(buff)
    sck.close()
    print('Download complete.')
    temp = prior_communications.get(hname, 0)
    prior_communications[hname] = temp + 1

def display_list(path):
    cluster = read_file(path)
    for i, (name, (ip, port)) in enumerate(cluster.items()):
        print('{}) Name: {} - IP Address: {} - Port: {}'.format(i+1, name, ip, port))

def get_random_port():
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.bind(('', 0))
    addr, port = sck.getsockname()
    sck.close()
    return port


if __name__ == "__main__":
    main(sys.argv[1:])
