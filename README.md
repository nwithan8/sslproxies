# SSLProxies

## Get free working proxy from <https://www.sslproxies.org/> and use it in your script

This is a port/rewrite of [free-proxy](https://github.com/jundymek/free-proxy) with additional features and validations.

SSLProxies pulls a list of free proxies from [sslproxies.org](https://www.sslproxies.org/)

You can choose to select a random proxy, or select a specific proxy by a set of criteria.

SSLProxies also features a ProxyManager that can be used to cache and reuse proxies, including managing their working
status.

Proxies are returned as objects with the following properties:

- ip: the IP address of the proxy
- port: the port of the proxy
- url: the full url of the proxy (this will always be HTTP regardless of the HTTPS status)
- country: the country of the proxy
- anonymity: the anonymity of the proxy
- https: whether the proxy supports https
- last_checked: the last time the proxy was checked
- last_working: the last time the proxy was working
- is_working: whether the proxy is working
- requests_dict: a pre-formatted dictionary object to be passed into a Requests library request

### Requirements

- Python3
- Request library
- BeautifulSoup library

### Installation

```python
pip install sslproxies
```

### Usage with examples

Get a random proxy:

```python
from sslproxies import ProxyManager

proxy = ProxyManager().get_new_proxy()
```

or

```python
from sslproxies import get_proxy

proxy = get_proxy()
```


Mark a proxy as working:

```python
from sslproxies import ProxyManager

proxy = ProxyManager().get_new_proxy()
manager = ProxyManager()
manager.mark_proxy_as_working(proxy)
```


## Options

```python
from sslproxies import get_proxy

proxy = get_proxy(countries=['US'], anonymous=True)
```

- **`countries` parameter**  
  Get a proxy from a specified list of countries. If there is no countries specified, proxies from all countries will be considered. Default ``countries=None``.

```python
proxy = get_proxy(countries=['US', 'BR', 'United States', 'Germany'])
```

- **`verify` parameter**  
  Return only a proxy that works (keeps testing proxies until one works). Default `verify=False`.

```python
proxy = get_proxy(verify=True)
```

- **`timeout` parameter**  
  During verification, if test site doesn't respond in X number of seconds, the proxy is considered non-working. Default `timeout=0.5`.

```python
proxy = get_proxy(timeout=1)
```

- **`rand` parameter**  
  Pull a random proxy, rather than the first one on the list. Default `rand=True`.

```python
proxy = get_proxy(rand=True)
```

- **`anonymous` parameter**  
  Return only those proxies that are marked as anonymous. Default `anonymous=False`.

```python
proxy = get_proxy(anonymous=True)
```

You can combine parameters:

```python
proxy = get_proxy(country_id=['US', 'BR'], timeout=0.3, rand=True, verify=True)
```

If there is no proxy matching all criteria, `get_proxy` returns `None`.

These same options are available in `get_new_proxy`, `get_non_working_proxy` and `get_cached_proxy` via the `ProxyManager`.
