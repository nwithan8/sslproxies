from typing import Union, List

from sslproxies.sslproxies import get_proxy_list, get_proxy, Proxy


class ProxyManager:
    def __init__(self):
        self._all_proxies = get_proxy_list()

    @property
    def _working_proxies(self) -> List[Proxy]:
        return [proxy for proxy in self._all_proxies if proxy.is_working]

    @property
    def _non_working_proxies(self) -> List[Proxy]:
        return [proxy for proxy in self._all_proxies if not proxy.is_working]

    @property
    def _untested_proxies(self) -> List[Proxy]:
        return [proxy for proxy in self._all_proxies if not proxy.last_working]

    def _find_matching_proxy_index(self, proxy: Proxy) -> Union[int, None]:
        for index, p in enumerate(self._all_proxies):
            if p.ip == proxy.ip and p.port == proxy.port:
                return index
        return None

    def test_all_proxies(self):
        """
        Test all proxies in the list. This will mark all proxies as working or not working. This will take a while.
        """
        for proxy in self._all_proxies:
            if proxy.check_if_working():
                self.mark_proxy_as_working(proxy)
            else:
                self.mark_proxy_as_not_working(proxy)

    def refresh_proxy_list(self):
        """
        Pull the latest proxy list from the website.
        """
        self.__init__()

    def get_cached_proxy(self, countries: List[str] = None, timeout: float = 0.5, https: bool = True, rand: bool = True,
                         anonymous: bool = False) -> Union[Proxy, None]:
        """
        Get a proxy marked as working from the cache.
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
        :return: Proxy object or None.
        :rtype: Union[Proxy, None]
        """
        if len(self._working_proxies) == 0:
            return None
        return get_proxy(countries=countries, timeout=timeout, https=https, rand=rand, anonymous=anonymous,
                         _proxy_list=self._working_proxies)

    def get_non_working_proxy(self, countries: List[str] = None, timeout: float = 0.5, https: bool = True,
                              rand: bool = True,
                              anonymous: bool = False) -> Union[Proxy, None]:
        """
        Get a proxy marked as non-working. Use this to retest proxies.
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
        :return: Proxy object or None.
        :rtype: Union[Proxy, None]
        """
        if len(self._untested_proxies) == 0:
            return None
        return get_proxy(countries=countries, timeout=timeout, https=https, rand=rand, anonymous=anonymous,
                         _proxy_list=self._non_working_proxies)

    def get_new_proxy(self, countries: List[str] = None, timeout: float = 0.5, https: bool = True, rand: bool = True,
                      anonymous: bool = False) -> Union[Proxy, None]:
        """
        Get a proxy that has not been tested yet.
        :param countries: List of countries to search for.
        :param timeout: Timeout for the request.
        :param https: Get a https proxy.
        :param rand: Get a random proxy.
        :param anonymous: Get an anonymous proxy.
        :return: Proxy object or None.
        :rtype: Union[Proxy, None]
        """
        if len(self._untested_proxies) == 0:
            return None
        return get_proxy(countries=countries, timeout=timeout, https=https, rand=rand, anonymous=anonymous,
                         _proxy_list=self._untested_proxies)

    def mark_proxy_as_working(self, proxy: Proxy):
        """
        Mark a proxy as working.
        :param proxy: Proxy object that is working.
        :type proxy: Proxy
        """
        index = self._find_matching_proxy_index(proxy)
        if index:
            self._all_proxies[index].mark_working()

    def mark_proxy_as_not_working(self, proxy: Proxy):
        """
        Mark a proxy as not working.
        :param proxy: Proxy object that is not working.
        :type proxy: Proxy
        """
        index = self._find_matching_proxy_index(proxy)
        if index:
            self._all_proxies[index].mark_not_working()
