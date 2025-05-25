import socket
import logging
import os
from multiprocessing import Pool, set_start_method
from file_protocol import FileProtocol
import concurrent.futures

fp = FileProtocol()

# Inisialisasi logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] [PID %(process)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Fungsi worker yang akan dijalankan oleh pool
def handle_client(conn, address):
    # client_address, data = payload
    # logging.warning(f"[Worker PID {os.getpid()}] Processing data from {client_address}")
    # hasil = fp.proses_string(data.strip()) + "\r\n\r\n"
    # return hasil
    logging.warning(f"Handle connection from {address}")
    try:
        data_rcv = ""
        while True:
            data = conn.recv(1024*1024)
            if not data:
                break
            logging.warning(f"Received chunk from {address}: {data[:50]}...")
            data_rcv += data.decode()
            while "\r\n\r\n" in data_rcv:
                cmd, data_rcv = data_rcv.split("\r\n\r\n", 1)
                hasil = fp.proses_string(cmd)
                response = hasil + "\r\n\r\n"
                conn.sendall(response.encode())
    
    except Exception as e:
        logging.error(f"[Main PID {os.getpid()}] Error handling client {address}: {e}")
    
    finally:
        conn.close()
        logging.warning(f"[Main PID {os.getpid()}] Connection closed for {address}")
    


class Server:
    def __init__(self, ipaddress='0.0.0.0', port=42331, worker_count=4):
        self.ipinfo = (ipaddress, port)
        self.worker_count = worker_count
        self.worker_count = worker_count
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        logging.warning(f"Server running on {self.ipinfo} with {self.worker_count} workers")
        self.my_socket.bind(self.ipinfo)
        self.my_socket.listen(1)

        with concurrent.futures.ProcessPoolExecutor(max_workers=self.worker_count) as executor:
            try:
                while True:
                    connection, address = self.my_socket.accept()
                    logging.warning(f"Accept connection from {address}")

                    executor.submit(handle_client, connection, address)
            except KeyboardInterrupt:
                logging.warning("Shutting down the server...")
            except Exception as e:
                logging.warning(f"Server Error: {e}")
            finally:
                if self.my_socket:
                    self.my_socket.close()


def main():
    server = Server(ipaddress='0.0.0.0', port=42331, worker_count=5)
    server.run()


if __name__ == "__main__":
    main()
