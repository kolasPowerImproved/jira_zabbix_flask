import requests
import json
import logging
from jira.client import JIRA
from flask import Flask, request
from pyzabbix import ZabbixAPI, ZabbixAPIException

from consts import SERVER_JIRA, PASSWORD_JIRA, LOGIN_JIRA, SERVER_ARP, USER_ARP, PASSWORD_ARP, SERVER_ZABBIX, \
    LOGIN_ZABBIX, PASSWORD_ZABBIX

app = Flask(__name__)


@app.route('/zabbix-add', methods=['POST', 'GET'])
def addHost():
    """
    This function used for adding new host with jira's issue
    :return: string
    """
    # get jira's issue name from the link
    issueName = request.args['key']
    #print(str(request.args))
    #print(issueName)

    # logging settings
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO,
                        filename=u'host_logs.log')

    if request.method == "POST":
        print(issueName)

        # connect to the jira
        jira_options = {'server': SERVER_JIRA}
        jira = JIRA(options=jira_options, basic_auth=(LOGIN_JIRA, PASSWORD_JIRA))
        issue = jira.issue(str(issueName))
        user = issue.fields.customfield_10001

        hostname = issue.fields.customfield_10001 + " - " + issueName

        # get ip from the jira login
        response = requests.post(SERVER_ARP, data={'username': USER_ARP, 'password': PASSWORD_ARP})
        token = json.loads(response.text)['token']
        response = requests.get('http://176.98.75.75:8002/api/abon_ip/%s/?Token=%s' % (user, token))
        ip = json.loads(response.text)['ip']

        # connect to the zabbix
        z = ZabbixAPI(SERVER_ZABBIX)
        z.login(user=LOGIN_ZABBIX, password=PASSWORD_ZABBIX)

        try:
            # create new host
            z.do_request(method="host.create", params={

                "host": hostname,

                "interfaces": [

                    {

                        "type": 1,

                        "main": 1,

                        "useip": 1,

                        "ip": ip,

                        "dns": "",

                        "port": "10050"

                    }

                ],

                "groups": [

                    {

                        "groupid": "37"

                    }

                ],

                "templates": [

                    {

                        "templateid": "10104"

                    }

                ],

            }

                         )
            #print("zbs")

            # logs writing
            info_str = 'Host ' + str(hostname) + ' successful added'
            logging.info(info_str)
        except ZabbixAPIException:
            ze = ZabbixAPIException('this host is already exist')
            # error logs
            err_str = 'Host ' + str(hostname) + ' is already exists'
            logging.error(err_str)
            print(ze)
    else:
        print('do not use POST method')
        # error connection logs
        err_str = 'Do not used true method. Must be used method POST'
        logging.error(err_str)

    return 'host added'


@app.route('/zabbix-remove', methods=['POST', 'GET'])
def removeHost():
    """
    This function used for removing host with host's name
    :return: string
    """
    # logging settings
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
            try:
                host_id = host[0]["hostid"]  #
                z.host.delete(host_id)  # delete host
                # deleting logs
                err_str = 'Host ' + hostname + ' successful removed'
                logging.info(err_str)
            except IndexError:
                out_of_range = IndexError("There is no host with this name")
                print(out_of_range)
                err_no_host_str = 'There is no host for delete' + hostname
                logging.error(err_no_host_str)
    else:
        print(' Do not used POST method')
        # connection error logs
        err_str = 'Do not used true method. Must be used method POST'
        logging.error(err_str)

    return 'host removed'


@app.route('/zabbix-update')
def updateHost():
    """
    This function used for updating existing host
    :return: string
    """
    # z.do_request(method="host.update", params={

     #   "hostid": "16847",

      #  "status": 1

    #}
    return None


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=6660)


