import re
from datetime import date
from urllib.request import urlopen

class BuildReport:
    def __init__(self):
        self.data = None
        self.failure_list = None
        self.most_recent_list = None
        self.most_recent_failures = None
        self.fails = None

    def create_fails(self):
        today = date.today()

        # get last month's builds too
        last_month = today.month - 1
        prev_month_year = today.year
        if last_month == 0:
            last_month = 12
            prev_month_year = prev_month_year - 1
        html_last_month = get_page(prev_month_year, last_month)
        failed_builds = get_failures_by_date(html_last_month)

        html_this_month = get_page(today.year, today.month)
        failed_builds.extend(get_failures_by_date(html_this_month))

        self.fails = failed_builds

    def create_most_recent_failures(self):
        self.most_recent_failures = self.fails[-1]

    def create_most_recent_list(self):
        self.most_recent_list = flatten(list(self.most_recent_failures.values()))

    def create_failure_list(self):
        failure_list = []
        for job in self.most_recent_list:
            earliest_failure_date = list(self.most_recent_failures.keys())[0]
            for failures in reversed(self.fails):
                if job in flatten(list(failures.values())):
                    earliest_failure_date = list(failures.keys())[0]
                else:
                    failure_list.append((job, earliest_failure_date))
                    break
        self.failure_list = failure_list

    def print_results(self):
        # Print new failures and failures by how long they've been failing for
        print("New failures today:\n")
        today = date.today()
        for (name, fail_date) in self.failure_list:
            if fail_date == str(today.year) + "-" + str(today.month) + "-" + str(today.day):
                print(name)

        print("\nFailures and first occurrence:\n")
        for (name, first_fail_date) in self.failure_list:
            print(first_fail_date + "\t" + name)


def flatten(nested_list):
    return [item for inner_list in nested_list for item in inner_list]

def get_failed_tasks(text):
    failed = re.findall("Failed Tasks:((.|\n)*?)(Succeeded|Pending)? Tasks:", text)
    as_list = failed[0][0].split("\n")
    jobs = [re.findall("^-.*", x) for x in as_list if len(re.findall("^-.*", x)) > 0]
    jobs = flatten(jobs)
    jobs = [x.strip(": ") for x in jobs]
    jobs = [x.strip("- ") for x in jobs]
    return jobs

def get_date(text):
    date = re.findall("Arrow Build Report for Job nightly-.*", text)[0]
    date = date.strip("Arrow Build Report for Job nightly-")
    date = date.strip("-0$")
    return date

def get_page(year, month):
    url = "https://mail-archives.apache.org/mod_mbox/arrow-builds/" + str(year) + str(month) + ".mbox"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    return html

def get_failures_by_date(html_content):
    split_by_day = html_content.split("Subject: [NIGHTLY] Arrow Build Report for Job nightly-")
    failures_by_date = [{get_date(x): get_failed_tasks(x)} for x in split_by_day[1:]]
    return failures_by_date











