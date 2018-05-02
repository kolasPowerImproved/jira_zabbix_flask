import jira
from jira.client import JIRA
from flask import Flask
import socket
import requests
import json
from flask import request
from jiraa.login_get import jiraGetUserFromTheIssue

from consts import SERVER_JIRA, PASSWORD_JIRA, LOGIN_JIRA


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'


@app.route('/jira')
def get_jira_login():
    jira_options = {'server': SERVER_JIRA}
    jira = JIRA(options=jira_options, basic_auth=(LOGIN_JIRA, PASSWORD_JIRA))
    issue = jira.issue('ZNET-21792')
    return issue.fields.customfield_10001


@app.route('/arp/')
def getIpFromLogin():
    user = jiraGetUserFromTheIssue('ZNET-21792')
    response = requests.post('http://176.98.75.75:8002/api/login/', data={'username': 'kolas', 'password': 'arp4443123505'})
    token = json.loads(response.text)['token']
    response = requests.get('http://176.98.75.75:8002/api/abon_ip/%s/?Token=%s' % (user, token))
    ip = json.loads(response.text)['ip']
    return ip

def func():
    get_jira_login()
    comment = jira.add_comment('JIRA-1330', 'new comment')

if __name__ == '__main__':
    app.run(debug=True)