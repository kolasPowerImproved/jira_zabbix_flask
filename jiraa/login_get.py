from consts import SERVER_JIRA, PASSWORD_JIRA, LOGIN_JIRA
import jira
from jira.client import JIRA

jira_options = {'server': SERVER_JIRA}

jira = JIRA(options=jira_options, basic_auth=(LOGIN_JIRA, PASSWORD_JIRA))

issue = jira.issue('ZNET-21792')

var = issue.fields.customfield_10001
print (issue.fields)

def jiraConnect(server, user, password):
    server = server
    user = user
    password = password
    jira_options = {'server': server}
    jira = JIRA(options=jira_options, basic_auth=(user, password))


def jiraGetUserFromTheIssue(issueName):
    issue = jira.issue(issueName)
    user = issue.fields.customfield_10001
    return user