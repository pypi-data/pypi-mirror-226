from multiprocessing.pool import ThreadPool

import click
import requests


class DirScanner(object):

    def __init__(self, base_url: str, status_codes: list[int]):
        self.base_url = base_url
        self.status_codes = status_codes

    def scan(self, directory_list: str, pool_size=2):
        with open(directory_list, 'r') as f:
            thread_pool = ThreadPool(processes=pool_size)
            while True:
                line = f.readline().strip()
                if line == '':
                    break
                thread_pool.apply_async(self.handle_directory, args=line)
            thread_pool.close()
            thread_pool.join()

    def handle_directory(self, directory: str) -> (int, str):
        url = f'{self.base_url}/{directory}'
        status_code = requests.get(url).status_code
        if self.is_status_code_positive(status_code):
            print(f'[+] {status_code} {url}')

    @staticmethod
    def get_status_code(url: str) -> int:
        return requests.get(f'{url}').status_code

    def is_status_code_positive(self, status_code: int) -> bool:
        return status_code in self.status_codes


@click.command()
@click.option(
    '--base-url',
    prompt='Enter the base url',
    help='the base url you want to scan',
    type=str
)
@click.option(
    '--dir-list',
    prompt='Enter the path to the directory list',
    help='the path to the directory list you want to use forthe scan',
    type=str
)
@click.option(
    '--status-codes',
    help='Enter the status codes you want to see',
    type=list[int],
    default=[200, 201, 203, 400, 401, 403],
    show_default=True
)
@click.option(
    '--pool-size',
    help='Enter the size of the thread pool',
    type=int,
    default=2,
    show_default=True
)
def main(base_url: str, dir_list: str, status_codes: list[int], pool_size: int) -> None:
    print('[+] directory scan started')
    print(f'[+] base url     : {base_url}')
    print(f'[+] dir list     : {dir_list}')
    print(f'[+] status codes : {status_codes}')
    print(f'[+] pool size    : {base_url}')
    scanner = DirScanner(base_url, status_codes)
    scanner.scan(dir_list, pool_size)
    print('[+] directory scan completed')


if __name__ == '__main__':
    main()
