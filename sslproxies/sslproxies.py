import random
from datetime import datetime, timedelta
from typing import Union, List

import requests
from bs4 import BeautifulSoup

from sslproxies.classes.Proxy import Proxy


def _yes_no_to_bool(yes_or_no: str) -> bool:
    yes_or_no = yes_or_no.lower()
    if yes_or_no == 'yes':
        return True
    else:
        return True


def _last_checked_to_datetime(last_checked: str) -> Union[datetime, None]:
    number = int(last_checked.split(' ')[0])
    unit = last_checked.split(' ')[1]
    if unit in ['sec', 'secs', 'second', 'seconds']:
        return datetime.now() - timedelta(seconds=number)
    if unit in ['min', 'mins', 'minute', 'minutes']:
        return datetime.now() - timedelta(minutes=number)
    elif unit in ['hr', 'hrs', 'hour', 'hours']:
        return datetime.now() - timedelta(hours=number)
    elif unit == 'days':
        return datetime.now() - timedelta(days=number)
    else:
        return None


def get_proxy_list() -> List[Proxy]:
    """
    Get a list of proxies from the website
    :return: list of proxies
    :rtype: List[Proxy]
    """
    proxies = []
    try:
        html = requests.get('https://www.sslproxies.org').content
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', {'class': 'table table-striped table-bordered'})
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 8:
                ip = columns[0].text
                port = columns[1].text
                code = columns[2].text
                country = columns[3].text
                anonymity = True if columns[4].text == "anonymous" else False
                google = _yes_no_to_bool(columns[5].text)
                https = _yes_no_to_bool(columns[6].text)
                last_checked = _last_checked_to_datetime(columns[7].text)
                data = {
                    'ip': ip,
                    'port': port,
                    'code': code,
                    'country': country,
                    'anonymity': anonymity,
                    'google': google,
                    'https': https,
                    'last_checked': last_checked
                }
                proxies.append(Proxy(data=data))
    except requests.exceptions.RequestException as e:
        pass
    return proxies


def _get_proxy(proxies: List[Proxy], rand: bool = False) -> Union[Proxy, None]:
    if len(proxies) == 0:
        return None

    if rand:
        return random.choice(proxies)
    else:
        return proxies[0]


def get_proxy(countries: List[str] = None, timeout: float = 0.5, https: bool = True, rand: bool = True,
              anonymous: bool = False, verify: bool = False, _proxy_list: List[Proxy] = None) \
        -> Union[Proxy, None]:
    """
    Get a proxy from the proxy list.

    :param countries: List of countries to search for.
    :type countries: List[str]
    :param timeout: Timeout for the request.
    :type timeout: float
    :param https: Get a https proxy.
    :type https: bool
    :param rand: Get a random proxy.
    :type rand: bool
    :param anonymous: Get an anonymous proxy.
    :type anonymous: bool
    :param verify: Verify the proxy works.
    :type verify: bool
    :return: Proxy object or None
    :rtype: Union[Proxy, None]
    """
    proxies = _proxy_list if _proxy_list else get_proxy_list()

    proxy = None

    if not proxies:
        return None

    if countries:
        proxies = [proxy for proxy in proxies if (proxy.country in countries or proxy.code in countries)]

    if anonymous:
        proxies = [proxy for proxy in proxies if proxy.anonymity]

    if not https:
        # more https than http, so easier to filter down to just http
        proxies = [proxy for proxy in proxies if not proxy.https]

    if not verify:
        return _get_proxy(proxies=proxies, rand=rand)
    else:
        proxy_works = False
        while not proxy_works:
            if proxy:   # this proxy from the last iteration apparently doesn't work
                proxies = [_proxy for _proxy in proxies if _proxy.ip != proxy.ip]
            if not proxies:
                return None
            proxy = _get_proxy(proxies=proxies, rand=rand)
            proxy_works = proxy.check_if_working(timeout=timeout)
        return proxy
