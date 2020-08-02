import os
import time
import socket
import datetime
import threading
import random as rnd

current_request_file = None
response_buffer = []
num_tcp_connections = 0

def main():
    global response_buffer, current_request_file
    
    list_file = 'list.txt'
    folder = './files/'
    interval = 5
    wait = 2
    connection_limit = 2

    udp_port = int(input('Enter UDP port: '))
    tcp_port = rnd.randint(12000, 13000)
    print('UDP listening on {}'.format(udp_port))
    print('TCP listening on {}'.format(tcp_port))
    

    tcp_receiver = threading.Thread(target=tcp_recv, args=(tcp_port, folder))
    udp_receiver = threading.Thread(target=udp_recv, args=(udp_port, list_file, folder, tcp_port, connection_limit))
    udp_sender = threading.Thread(target=udp_send_discovery, args=(udp_port, list_file, interval))
    udp_receiver.start()
    udp_sender.start()
    tcp_receiver.start()

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
            udp_send_gett(filename, list_file, udp_port)
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
            port, ip = l.split(' ')
            cluster[int(port)] = ip
    return cluster

def update_file(new_cluster, path, udp_port):
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

def build_message(dic, my_port):
    st = 'Disc {}\n'.format(my_port)
    for port, ip in dic.items():
        st += '{} {}\n'.format(port, ip)
    return st.strip()


# ---------------------------------------------------------------
# These functions are used for sending, receiving
# and processing different udp and tcp requests.
# ---------------------------------------------------------------

def tcp_recv(tcp_port, folder):
    global num_tcp_connections
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.bind(('', tcp_port))
    sck.listen(5)
    while True:
        connection, addr = sck.accept()
        num_tcp_connections += 1
        filename = connection.recv(1024).decode('utf-8')
        with open(folder + filename, 'r') as f:
            l = f.read(1024)
            while l:
                connection.send(l.encode('utf-8'))
                l = f.read(1024)
        connection.shutdown(socket.SHUT_WR)
        num_tcp_connections -= 1

def udp_recv(udp_port, path, folder, tcp_port, connection_limit):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.bind(('', udp_port))
    while True:
        msg, addr = sck.recvfrom(1024)
        msg = msg.decode('utf-8')
        msg_type = msg[:4]
        
        if msg_type == 'Disc':
            cluster, port = extract_data(msg)
            cluster.update({port: addr[0]})
            update_file(cluster, path, udp_port)

        elif msg_type == 'Gett':
            if num_tcp_connections < connection_limit:
                udp_send_resp(msg, addr, folder, tcp_port)

        elif msg_type == 'Resp':
            save_resp(msg, addr)

        else:
            print('Message format not supported.')

def udp_send_discovery(udp_port, path, interval):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        cluster = read_file(path)
        data = build_message(cluster, udp_port)
        for port, ip in cluster.items():
            sck.sendto(data.encode('utf-8'), (ip, port))
        time.sleep(interval)

def udp_send_gett(filename, list_file, my_port):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    nodes = read_file(list_file)
    msg = 'Gett {} {}'.format(filename, my_port)
    print('\nGet message sent to:')
    for node in nodes.items():
        sck.sendto(msg.encode('utf-8'), (node[1], node[0]))
        print('   {}:{}'.format(node[1], node[0]))
    print()

def udp_send_resp(msg, source, folder, tcp_port):
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = msg.strip()[5:]
    filename, destination_port = msg.split(' ')
    destination_port = int(destination_port)
    if not os.path.exists(folder):
        return
    files = os.listdir(folder)
    for file in files:
        if file == filename:
            msg = build_get_response(filename, tcp_port)
            sck.sendto(msg.encode('utf-8'), (source[0], destination_port))
            return

def save_resp(msg, source):
    global current_request_file, response_buffer
    msg = msg.strip()[5:]
    port, sent_time, filename = msg.split('\n')
    sent_time = datetime.datetime.strptime(sent_time, '%Y-%m-%d %H:%M:%S.%f')
    if filename == current_request_file:
        delay = (datetime.datetime.now() - sent_time).total_seconds()
        response_buffer.append((source[0], int(port), delay))

def build_get_response(filename, tcp_port):
    now = datetime.datetime.now()
    msg = 'Resp {}\n{}\n{}'.format(tcp_port, now, filename)
    return msg     

def find_best_candidate():
    global response_buffer
    if len(response_buffer) == 0:
        print('File wasn\'t found.')
        return None
    print('File was found on:')
    for res in response_buffer:
        print('  {}:{} with delay {} seconds'.format(res[0], res[1], res[2]))
    response_buffer.sort(key=lambda x:x[1])
    best = response_buffer[0]
    print('\nDownloading from {}:{} ...'.format(best[0], best[1]))
    return best

def download_from(filename, host, folder):
    buff = 1024
    ip, port = host[0], host[1]
    tcp_send_sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_send_sck.connect((ip, port))
    tcp_send_sck.send(filename.encode('utf-8'))
    with open(folder + filename, 'w') as f:
        l = tcp_send_sck.recv(buff).decode('utf-8')
        while l:
            f.write(l)
            l = tcp_send_sck.recv(buff).decode('utf-8')
    tcp_send_sck.close()
    print('Download complete.')

def display_list(path):
    cluster = read_file(path)
    for i, (port, ip) in enumerate(cluster.items()):
        print('{}) IP Address: {} - Port: {}'.format(i+1, port, ip))



if __name__ == "__main__":
    main()
