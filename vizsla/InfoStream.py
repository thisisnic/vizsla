from abc import ABC, abstractmethod
from datetime import datetime
import requests


class InfoStream(ABC):
    def __init__(self, cache=None):
        # Cache is a {datetime: array} dict where datetime is the datetime of retrieval and the array is the results
        self.cache = cache
        # When we build in mechanisms to update from the cache, this value is updated upon successful retrieval
        self.last_updated = None


class JIRAStream(InfoStream):
    def __init__(self):
        super().__init__()


class JIRAIssueList(JIRAStream):
    def __init__(self, url):
        self.url = url
        super().__init__()

    def get_issues(self):
        return self.cache

    def __update_issues(self):
        """
        Update issues in the cache
        :return:
        """
        update_time, new_issues = self.__fetch_issues()
        cache_entry = [{update_time: new_issues}]
        self.cache = cache_entry + self.cache
        self.last_updated = update_time

    def __fetch_issues(self):
        """
        Fetch issues from the URL
        :return: time the issues were retrieved, and the parsed issues
        """
        update_time = datetime.now()
        response = requests.get(self.url)
        if response.ok:
            parsed_issues = self.__parse_issues(response.json()["issues"])
            return update_time, parsed_issues
        else:
            raise RuntimeError("API response was not OK!")

    def __parse_issues(self, issues):
        """
        Convert issues to correct format
        :param issues:
        :return:
        """
        parsed_issues = issues
        return parsed_issues


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


class GitHubStream(InfoStream):
    def __init__(self):
        super().__init__()
