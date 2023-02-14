import os

from jira_dump import Dumper, IssueField


class CustomDumper(Dumper):
    assignee = IssueField(["fields", "assignee", "displayName"])
    reporter = IssueField(["fields", "reporter", "displayName"])
    # fixme: these will not be the same for you
    sla = IssueField(["fields", "customfield_11900"])
    maintenance_type = IssueField(["fields", "customfield_10300", "value"])
    module = IssueField(["fields", "customfield_10207", "value"])
    fix_versions = IssueField(["fields", "fixVersions"])

    last_update_date = IssueField(["fields", "updated"])

    get_transitions = False
    get_comments = False
    get_fix_versions = True

    def unreleased_project_versions(self, project):
        return filter(lambda x: not x.released, self.jira.project_versions(project))


def issue_dumper(dumper):
    _dumper = dumper

    def _issues(jql):
        _dumper.jql = jql
        with _dumper:
            yield from _dumper.issues

    return _issues


def read_password():
    with open(os.environ["JIRA_PASSWORD_FILE"], mode="r", encoding="utf-8") as file:
        return file.read().strip()


jira_dumper: Dumper = CustomDumper(
    server=os.environ["JIRA_URL"],
    jql="",
    auth=(os.environ["JIRA_USER"], read_password()),
)


jira_issues = issue_dumper(jira_dumper)
