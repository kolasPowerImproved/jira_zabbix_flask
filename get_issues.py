import requests
import json
import logging
import re
import pprint
from jira.client import JIRA
from flask import Flask, request
from pyzabbix import ZabbixAPI, ZabbixAPIException

from consts import SERVER_JIRA, PASSWORD_JIRA, LOGIN_JIRA, SERVER_ARP, USER_ARP, PASSWORD_ARP, SERVER_ZABBIX, \
    LOGIN_ZABBIX, PASSWORD_ZABBIX

file = open("JIRA.csv", "r")
a_str = file.read()
file.close()
a_list = a_str.split('\n')
j_mn = set(a_list)

file = open("1.txt", "r")
h_str = file.read()
file.close()
h_list = h_str.split('\n')
z_mn = set(h_list)

d_mn = []

d_mn = z_mn - j_mn

z = ZabbixAPI(SERVER_ZABBIX)
z.login(user=LOGIN_ZABBIX, password=PASSWORD_ZABBIX)

i = 0

for host in d_mn:
    result = z.do_request(method="host.get", params={
        "search": {
            "name": host
        },
        "output": "hostid"
    }

                          )
    i += 1
    print(host)
    print(i)
   # print(result['result'][0]['hostid'])
    try:
      z.host.delete(result['result'][0]['hostid'])
    except IndexError:
        continue
