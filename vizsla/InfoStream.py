from abc import ABC, abstractmethod
from datetime import datetime
import requests

from Issue import Issue, PR


class InfoStream(ABC):
    def __init__(self):
        pass


class JIRAStream(InfoStream):
    def __init__(self):
        super().__init__()


def parse_issue(issue):
    """
    Convert issues to correct format
    :param issue:
    :return:
    """
    issue_fields = issue.get("fields")

    issue_id = issue.get("key")
    name = issue_fields.get("summary")
    description = issue_fields.get("description")
    status = issue_fields.get("status")
    if status is not None:
        status = status.get("name")
    priority = issue_fields.get("priority")
    if priority is not None:
        priority = priority.get("name")
    assignee = issue_fields.get("assignee")
    if assignee is not None:
        assignee = assignee.get("name")
    reporter = issue_fields.get("reporter")
    if reporter is not None:
        reporter = reporter.get("name")

    return Issue(issue_id, name, description, status, priority, assignee, reporter)


def parse_pr(pr):
    return PR(pr.get("html_url"), pr.get("number"), pr.get("title"))


class JIRAIssueList(JIRAStream):
    def __init__(self, url):
        self.url = url
        super().__init__()

    def get_issues(self):
        """
        Fetch issues from the URL
        :return: time the issues were retrieved, and the parsed issues
        """

        print("Trying URL: " + self.url)
        response = requests.get(self.url)
        if response.ok:
            parsed_issues = [parse_issue(issue) for issue in response.json().get("issues")]
            return parsed_issues
        else:
            raise RuntimeError("API response was not OK!")


class JIRASearchIssueList(JIRAIssueList):
    """
    Gets list of issues relating to a particular JQL query
    """

    def __init__(self, jql):
        url = jira_api_query(jql)
        super().__init__(url)


class JIRAUserIssueList(JIRAIssueList):
    """
    Gets list of issues relating to a particular user
    """

    def __init__(self, user):
        self.user = user
        jql = "assignee%20%3D%20" + user + \
              "%20%20AND%20resolution%20%3D%20Unresolved%20order%20by%20updated%20DESC"
        url = jira_api_query(jql)
        super().__init__(url)


def jira_api_query(jql):
    intro_string = "https://issues.apache.org/jira/rest/api/2/search?jql="
    return intro_string + jql


def github_api_query(query):
    intro_string = "https://api.github.com/"
    return intro_string + query


class GitHubStream(InfoStream):
    def __init__(self):
        super().__init__()


class GitHubPullsStream(GitHubStream):
    def __init__(self, query):
        super().__init__()
        self.query = query
        self.url = github_api_query(query)

    def get_prs(self):
        """
        Fetch issues from the URL
        :return:
        """

        print("Trying URL: " + self.url)
        response = requests.get(self.url)
        if response.ok:
            parsed_prs = [parse_pr(pr) for pr in response.json()]
            return parsed_prs
        else:
            raise RuntimeError("API response was not OK!")
