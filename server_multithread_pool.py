from socket import *
import socket
import threading
import logging
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from file_protocol import FileProtocol

from file_protocol import  FileProtocol
fp = FileProtocol()

MAX_WORKERS=50

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(processName)s/%(threadName)s] - %(message)s'
)

class ProcessTheClient:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.fp = FileProtocol()
        # threading.Thread.__init__(self)

    def handle(self):
        logging.warning(f"Handling client {self.address}")
        data_rcv = ""
        while True:
            data = self.connection.recv(1024*1024)
            if data:
                decoded_chunk = data.decode()
                logging.warning(f"potongan data diterima: {decoded_chunk[:80]}...")
                data_rcv += decoded_chunk
                if "\r\n\r\n" in data_rcv:
                    break
            else:
                break
        
        if data_rcv:
            hasil = fp.proses_string(data_rcv.strip())
            hasil += "\r\n\r\n"
            self.connection.sendall(hasil.encode())

        self.connection.close()


class Server:
    def __init__(self,ipaddress='0.0.0.0',port=8889, max_workers=10):
        self.ipinfo=(ipaddress,port)
        # self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.max_workers = max_workers
        # threading.Thread.__init__(self)

    def start(self):
        logging.warning(f"server berjalan di ip address {self.ipinfo}")
        self.my_socket.bind(self.ipinfo)
        self.my_socket.listen(10)
        logging.warning(f'Number of workers: {self.max_workers}')
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while True:
                connection, client_address = self.my_socket.accept()
                logging.warning(f"connection from {client_address}")

                handler = ProcessTheClient(connection, client_address)
                executor.submit(handler.handle)
    
                # clt = ProcessTheClient(self.connection, self.client_address)
                # clt.start()
                # self.the_clients.append(clt)


def main():
    svr = Server(ipaddress='0.0.0.0',port=42331, max_workers=MAX_WORKERS)
    svr.start()


if __name__ == "__main__":
    main()

