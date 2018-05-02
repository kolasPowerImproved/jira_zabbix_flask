import requests
import json
import logging
from jira.client import JIRA
from flask import Flask, request
from pyzabbix import ZabbixAPI, ZabbixAPIException

from consts import SERVER_JIRA, PASSWORD_JIRA, LOGIN_JIRA, SERVER_ARP, USER_ARP, PASSWORD_ARP, SERVER_ZABBIX, \
    LOGIN_ZABBIX, PASSWORD_ZABBIX

# logging settings
def func():
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                        filename=u'host_logs.log')

    # get jira's issue name from the link
    issueName = request.args['key']

    # connect to the zabbix
    z = ZabbixAPI(SERVER_ZABBIX)
    z.login(user=LOGIN_ZABBIX, password=PASSWORD_ZABBIX)

    # connect to the jira
    jira_options = {'server': SERVER_JIRA}
    jira = JIRA(options=jira_options, basic_auth=(LOGIN_JIRA, PASSWORD_JIRA))
    issue = jira.issue(str(issueName))
    hostname = issue.fields.customfield_10001 + " - " + issueName

    if request.method == "POST":
        try:
            host = z.host.get(filter={"host": hostname})
        except ZabbixAPIException:
            ze = ZabbixAPIException('No permissions to referred object or it does not exist!')
            print(ze)
            # permission error logs
            err_str = 'No permissions to referred object or it does not exist! ' + hostname
            logging.error(err_str)
        else:
            host_id = host[0]["hostid"]    #
            try:
               z.host.delete(host_id)         # delete host
               # deleting logs
               err_str = 'Host ' + hostname + ' successful removed'
               logging.info(err_str)
            except IndexError:
                out_of_range = IndexError("There is no host with this name")
                err_no_host_str = 'There is no host' + hostname
                logging.error(err_no_host_str)
    else:
        print(' Do not used POST method')
        # connection error logs
        err_str = 'Do not used true method. Must be used method POST'
        logging.error(err_str)