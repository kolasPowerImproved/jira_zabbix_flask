from pyzabbix import ZabbixAPI

from consts import SERVER_ZABBIX, LOGIN_ZABBIX, PASSWORD_ZABBIX

z = ZabbixAPI(SERVER_ZABBIX)

z.login(user=LOGIN_ZABBIX, password=PASSWORD_ZABBIX)

host = z.host.get(filter={"host": "zazazaz11331111azaz"})
if host:
    host_id = host[0]["hostid"]
    print("Found host id {0}".format(host_id))

