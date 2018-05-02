from pyzabbix import ZabbixAPI

from consts import SERVER_ZABBIX, LOGIN_ZABBIX, PASSWORD_ZABBIX

z = ZabbixAPI(SERVER_ZABBIX)

z.login(user=LOGIN_ZABBIX, password=PASSWORD_ZABBIX)

z.do_request(method="host.update", params={

    "hostid": "16847",

    "status": 1

}

             )