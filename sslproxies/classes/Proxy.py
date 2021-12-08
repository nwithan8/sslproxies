from datetime import datetime

import requests


class Proxy:
    def __init__(self, data):
        self._data = data
        self.ip = data['ip']
        self.port = data['port']
        self.code = data['code']
        self.country = data['country']
        self.anonymity = data['anonymity']
        self.google = data['google']
        self.https = data['https']
        self.last_checked = data['last_checked']
        self.is_working = False
        self.last_working = None

    @property
    def ip_and_port(self):
        return f'{self.ip}:{self.port}'

    @property
    def url(self):
        return f'http://{self.ip_and_port}'

    @property
    def is_anonymous(self):
        return self.anonymity

    @property
    def requests_dict(self):
        return {'http': self.url}

    def mark_working(self):
        self.last_checked = datetime.now()
        self.last_working = datetime.now()
        self.is_working = True

    def mark_not_working(self):
        self.last_checked = datetime.now()
        self.is_working = False

    def check_if_working(self, timeout: float = 0.5) -> bool:
        try:
            if not self.https:
                print("HTTP")
            # make request with proxy and check if response connection has proxy
            with requests.get('http://www.google.com', proxies=self.requests_dict, timeout=timeout, stream=True) as r:
                if r.raw.connection.sock:
                    peername = r.raw.connection.sock.getpeername()
                    if peername[0] == self.ip:
                        self.mark_working()
                        return True
        except Exception as e:
            pass
        self.mark_not_working()
        return False
