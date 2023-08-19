# getownip - A python script to determine your ip address

Example:

```python
import getownip
print("public IPv4: " + getownip.get(getownip.Public, getownip.IPv4))
print("local IPv6: " + getownip.get(getownip.Local, getownip.IPv6))
```

To retrieve a local ip address, a default route must exist. Otherwise, `None` is returned.

When retrieving a public ip address, a random one of a list of servers is accessed.
Currently, the following list of servers is used:

| service       | IPv4 | IPv6 |
|---------------|------|------|
| ipv4.cf       |  yes |      |
| icanhazip.com |  yes |  yes |
| ipaddress.com |  yes |      |
| getmyip.dev   |  yes |  yes |
| ipinfo.io     |  yes |      |
| l2.io         |  yes |      |
| my-ip.io      |  yes |  yes |
| ident.me      |  yes |  yes |
| ipify.org     |  yes |  yes |
| seeip.org     |  yes |  yes |

If one of these services fails to answer, another one will be tried until every service has failed.
In this case, the last occurred exception will be thrown.
