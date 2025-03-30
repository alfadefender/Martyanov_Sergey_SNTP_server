import socket
import struct
import time
from extra import LOCAL_SNTP_SERVER, GOOGLE_SNTP_SERVER, to_binary

SERVER_HOST = LOCAL_SNTP_SERVER
SERVER_PORT = 123


def get_sntp_time():
    sntp_request = b'\x23' + 47 * b'\0' # SNTP заголовок для клиента

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(sntp_request, (SERVER_HOST, SERVER_PORT))

        response, _ = client_socket.recvfrom(1024)

        response_bytes = []

        for byte in response:
            response_bytes += [to_binary(byte)]

        seconds = int("".join(response_bytes[40:44]), 2)
        fraction = int("".join(response_bytes[44:48]), 2)

        recived_time = seconds - 2208988800 + fraction / float(2**32)

        print(f"Точное время в секундах: {recived_time}")
        print(f"Полученное время с сервера: {time.ctime(abs(recived_time))}")
        print(f"Время с ОС: {time.ctime(time.time())}")


if __name__ == '__main__':
    get_sntp_time()
