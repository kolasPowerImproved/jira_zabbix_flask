from pyzabbix import ZabbixAPI

class ZabbixConnect():
    def connect(self, server, login, password):
        z = ZabbixAPI(server)
        z.login(user=login, password=password)
