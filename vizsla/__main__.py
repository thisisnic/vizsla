from InfoStream import JIRASearchIssueList

if __name__ == '__main__':

    r_issues = JIRASearchIssueList('project%20%3D%20ARROW%20AND%20resolution%20%3D%20Unresolved%20AND%20('
                                   'summary%20~%20%22%5C%5C%5BR%5C%5C%5D%22%20OR%20component%20%3D%20R%20)%20ORDER'
                                   '%20BY%20created%20DESC%2C%20priority%20DESC%2C%20updated%20DESC')


    print(r_issues.get_issues())

