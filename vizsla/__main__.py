from InfoStream import JIRASearchIssueList, GitHubPullsStream
from BuildReport import BuildReport
import sys


def run_nightlies():
    nightlies = BuildReport()
    nightlies.print_failure_dates()


if __name__ == '__main__':

    if len(sys.argv) >= 2:
        if sys.argv[1] == "nightlies":
            run_nightlies()

    else:
        # run everything!
        run_nightlies()

    # print("***************************************************************")
    # r_issues = JIRASearchIssueList('project%20%3D%20ARROW%20AND%20resolution%20%3D%20Unresolved%20AND%20('
    #                               'summary%20~%20%22%5C%5C%5BR%5C%5C%5D%22%20OR%20component%20%3D%20R%20)%20ORDER'
    #                               '%20BY%20created%20DESC%2C%20priority%20DESC%2C%20updated%20DESC')

    # [print(issue) for issue in r_issues.get_issues()]

    # print("***************************************************************")
    # r_approved_not_merged = GitHubPullsStream('/repos/apache/arrow/pulls?q=is%3Aopen+is%3Apr+review%3Aapproved+"[R]"+in%3Atitle')
    # [print(pr) for pr in r_approved_not_merged.get_prs()]
