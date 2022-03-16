class Issue:
    def __init__(self, issue_id, name, description, status, priority, assignee, reporter):
        self.priority = priority
        self.reporter = reporter
        self.name = name
        self.assignee = assignee
        self.status = status
        self.description = description
        self.issue_id = issue_id

    def __str__(self):
        return str(self.issue_id + ": " + self.name)


class PR:
    def __init__(self, html_url, number, title):
        self.url = html_url
        self.number = number
        self.title = title

    def __str__(self):
        return str(self.title + " | " + self.url)
