"""
Стандартная реализация SNTP-сервера

Используется конфигурационный файл "config.cfg", в котором могут быть:
1). адрес сервера (опционально)
2). количество секунд на которые он врет
Каждое поле идет отдельно и по описанному порядку.

Используются модули:
1). socket (встроенный)
2). time (встроенный)
3). extra

"""


import socket
import time
from extra import to_hex_list


def get_sntp_response(lied_secs=0):
    current_time = time.time() + lied_secs
    seconds = int(current_time)
    fraction = int((current_time - seconds) * 2 ** 32)

    # Время в секундах с 1900 года
    timestamp = seconds + 2208988800

    response = bytearray(48)
    response[0:4] = b'\x24\x01\x04\xFA'
    response[4:16] = b'\0' * 12
    response[16:20] = to_hex_list(timestamp)
    response[20:40] = b'\0' * 20
    response[40:44] = to_hex_list(timestamp)
    response[44:48] = to_hex_list(fraction)

    return response


def start_sntp_server(host='localhost', port=123, lied_secs=0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
            server_socket.bind((host, port))

            print(f"SNTP сервер запущен на {host}:{port}")

            while True:
                data, addr = server_socket.recvfrom(1024)

                print(f"Получен запрос от {addr}")

                response = get_sntp_response(lied_secs)
                server_socket.sendto(response, addr)
                print(f"Ответ отправлен: {addr}")

    except Exception as e:
        print("Runtime Exception")


def setup_from_cfg() -> list:
    result_params = ["localhost", 123, 0]
    params = []
    with open("config.cfg") as cfg:
        for line in cfg:
            params += [line]

    if not params:
        return result_params

    elif len(params) == 1:
        try:
            n = int(params[0])
            result_params[2] = n

        except Exception as e:
            print("Warning: Invalid config")

        return result_params

    elif len(params) == 2:
        try:
            n = int(params[1])
            result_params[0] = params[0]
            result_params[2] = n

        except Exception as e:
            print("Warning: Invalid config")

        return result_params

    print("Warning: Invalid config")
    return result_params


if __name__ == '__main__':
    host, port, lied_secs = setup_from_cfg()
    start_sntp_server(host, port, lied_secs)
