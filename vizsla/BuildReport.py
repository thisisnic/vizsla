import re
from datetime import date, timedelta
from urllib.request import urlopen


class BuildReport:
    def __init__(self):
        self.data = {}

    def print_failure_dates(self):
        failure_list = self.get_failure_date_list()
        # Print new failures and failures by how long they've been failing for
        print("New failures today:\n")

        for (name, fail_date) in failure_list:
            if fail_date == date.today().strftime("%Y-%m-%d"):
                print(name)

        print("\nFailures and first occurrence:\n")
        for (name, first_fail_date) in failure_list:
            print(first_fail_date + "\t" + name)

    def get_failure_date_list(self):

        fails = self.get_failed_builds()
        # Get the most recent day's data, i.e. the last element
        most_recent_failures = fails[-1]

        most_recent_list = flatten(list(most_recent_failures.values()))
        # initialise empty list
        failure_list = []

        # for each job, e.g. "verify-rc-source-windows"
        for job in most_recent_list:
            # set the earliest failure date to the date in question (likely today!)
            earliest_failure_date = list(most_recent_failures.keys())[0]
            # go through the list of failures in reverse order (i.e. from most recent to longest ago)
            for failures in reversed(fails):
                # if the job is in that list, then set the earliest failure date to that date
                if job in flatten(list(failures.values())):
                    earliest_failure_date = list(failures.keys())[0]
                # if it's not in that list, then we are assuming it has passed so add that date as the earliest
                # failure date ** FIX THIS!! not failed doesn't mean passed; could have been pending! **
                else:
                    failure_list.append((job, earliest_failure_date))
                    break

        return failure_list

    def get_failed_builds(self):
        """
        Get list of failed builds for this and last month
        """
        this_month, last_month = get_date_strings()

        failed_builds = self.get_failures_by_date(last_month)
        failed_builds.extend(self.get_failures_by_date(this_month))

        return failed_builds

    def get_failures_by_date(self, month):
        """
        Get the list of failures for a particular month
        :param month: Month to report on
        :return: List of {date: [failures]} dicts
        """
        self.fetch_data(month)

        # Get the HTML data for that month
        html_content = self.data[month]
        # drop the first element as it's just the header
        split_by_day = html_content.split("Subject: [NIGHTLY] Arrow Build Report for Job nightly-")[1:]
        # Return [{"date": ["failures", "list"]}] for that date
        failures_by_date = [{extract_date(x): extract_failed_tasks(x)} for x in split_by_day]
        return failures_by_date

    def fetch_data(self, month, override=False):
        """
        If the data for that month hasn't been fetched, fetch it
        :param override: Override the check for if data already exists
        :param month: Month in %Y%m format, e.g. "202202"
        """
        if month not in self.data and not override:
            url = "https://mail-archives.apache.org/mod_mbox/arrow-builds/" + str(month) + ".mbox"
            page = urlopen(url)
            html_bytes = page.read()
            self.data[month] = html_bytes.decode("utf-8")

        return self.data[month]


def extract_date(text):
    """
    Given the HTML text for one day, get the date
    :param text: HTML text for one day
    :return: Date as string
    """
    report_date = re.findall("Arrow Build Report for Job nightly-.*", text)[0]
    report_date = report_date.strip("Arrow Build Report for Job nightly-")
    report_date = report_date.strip("-0$")
    return report_date


def extract_failed_tasks(text):
    """
    Given the HTML text for one day, get the failed tasks for that day
    :param text: HTML text for one day
    :return: List of failed task names
    """

    # Get all tasks in the section starting with "Failed Tasks" until we get up to "Succeeded" or "Pending"
    failed = re.findall("Failed Tasks:((.|\n)*?)(Succeeded|Pending)? Tasks:", text)
    # This is an array containing a tuple; take the first element and split it by newline to get individual build
    # failures
    jobs = failed[0][0].split("\n")
    # Job names are in the lines starting with "- "; extract them
    jobs = [re.findall("^-.*", x)[0] for x in jobs if len(re.findall("^-.*", x)) > 0]
    # Strip out extra characters
    jobs = [x.strip(": ").strip("- ") for x in jobs]
    return jobs


# This is suboptimal - we should recode this to only retrieve last
# month's data if we have a failing build which we don't know it's first
# failure date
def get_date_strings():
    """
    Get date strings for last month and this month in "%Y%m" format, e.g. "202201"
    """
    today = date.today()
    first = today.replace(day=1)
    last_month = first - timedelta(days=1)

    this_month_string = today.strftime("%Y%m")
    last_month_string = last_month.strftime("%Y%m")
    return this_month_string, last_month_string


# Factor out uses of this function
def flatten(nested_list):
    return [item for inner_list in nested_list for item in inner_list]
