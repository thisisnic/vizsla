# Vizsla

Retrieve items from various sources which are useful for day-to-day maintainer tasks.  Designed to work with:
* JIRA API
* GitHub API
* Arrow nightly builds email digest

WIP - but you can get the nightly build digest running by running the main method.  Example output:

```
New failures today:

test-ubuntu-18.04-r-sanitizer
verify-rc-source-cpp-macos-amd64
verify-rc-source-integration-linux-ubuntu-20.04-amd64

Failures and first occurrence:

2022-03-17	test-ubuntu-18.04-r-sanitizer
2022-03-17	verify-rc-source-cpp-macos-amd64
2022-03-17	verify-rc-source-integration-linux-ubuntu-20.04-amd64
2022-03-16	centos-8-stream-amd64
2022-03-16	centos-8-stream-arm64
2022-03-15	verify-rc-source-integration-linux-conda-latest-amd64
2022-03-14	test-r-linux-valgrind
2022-03-13	conda-win-vs2017-py37-r41
2022-03-13	conda-win-vs2017-py38
2022-03-03	test-r-linux-as-cran
```

## Name

The project is named after the dog breed - a lean yet robust retriever.