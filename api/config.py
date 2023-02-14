import re

project_key = "AYY"

# uses Jira SLA plugin
sla_regex = re.compile(
    r"""AYY[ ]SLA[ ]P.: # will be project specific
        (-)?            # matches whether sla is still OK, or failed
        ((.+?)(d))*[ ]* # matches day part
        ((.+?)(h))*[ ]* # matches hour part
        ((.+?)(m))*[ ]* # matches minute part
        ((.+?)(s))*     # matches second part""",
    re.VERBOSE,
)

# JQL
# project = AYY AND type = Issue AND status not in (Accepted, Cancelled, Cancelled, Closed, "In Testing", "Solution Delivered", "Waiting Information", Tested)
jira_maintenance_filter_id = 15509
# project = AYY AND status = Tested
jira_tested_filter_id = 15510
# project = AYY AND fixVersion in unreleasedVersions()
jira_fix_version_filter_id = 15511

project = "Project Name in Jira"

tested = "Tested"
delivered = "Solution Delivered"

good_statuses = (
    "Accepted/Answered",
    "In Estimation",
    "In Progress",
    "Open",
    "In Delivery",
    "Re-estimate",
)
