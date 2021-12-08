import freeproxy

manager = freeproxy.ProxyManager()
manager.test_all_proxies()
new_proxy = manager.get_cached_proxy()
if new_proxy.check_if_working():
    manager.mark_proxy_as_working(new_proxy)
    print("Proxy is working")
else:
    manager.mark_proxy_as_not_working(new_proxy)
    print("Proxy is not working")

