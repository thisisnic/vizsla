import requests


def get_users_open_issues(user):
    url = "https://issues.apache.org/jira/rest/api/2/search?jql=assignee%20%3D%20" + \
          user + "%20%20AND%20resolution%20%3D%20Unresolved%20order%20by%20updated%20DESC"
    response = requests.get(url)
    return response.json()


def get_new_r_tickets():
    r_tickets_url = "https://issues.apache.org/jira/rest/api/2/search?jql=project%20%3D%20ARROW%20AND%20resolution%20" \
                    "%3D%20Unresolved%20AND%20(" \
                    "summary%20~%20%22%5C%5C%5BR%5C%5C%5D%22%20OR%20component%20%3D%20R%20)%20ORDER%20BY%20created" \
                    "%20DESC%2C%20priority%20DESC%2C%20updated%20DESC "
    response = requests.get(r_tickets_url)
