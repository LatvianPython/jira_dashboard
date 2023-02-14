import datetime

import dateutil.parser

import config


def parse_sla(sla_string):
    try:
        match = config.sla_regex.match(sla_string)
        if match[1] == "-":
            sign = -1
        else:
            sign = 1
        sla_time = 0
        multipliers = [24 * 60 * 60, 60 * 60, 60, 1]
        for i, multiplier in enumerate(multipliers, start=1):
            try:
                sla_time += int(match[i * 3]) * multiplier
            except TypeError:
                pass

        day_part = match[2]
        if day_part is not None and int(match[3]) >= 4:
            sla_text = "More than " + day_part.replace("d", " days")
        else:
            sla_text = " ".join(
                filter(lambda x: x is not None, (match[i * 3 - 1] for i in range(1, 4)))
            )

        if sign < 0:
            sla_text += " Overdue"
        else:
            sla_text += " Left"

        return sla_text, sla_time * sign
    except AttributeError:
        return 999999999


def seconds_to_text(seconds):
    text = ""
    multipliers = {"w": 60 * 60 * 8 * 5, "d": 60 * 60 * 8, "h": 60 * 60, "m": 60}
    for key, multiplier in multipliers.items():
        dist = int(seconds / multiplier)
        seconds -= dist * multiplier
        if dist > 0:
            text += str(dist) + key + " "

    return text or "0m"


def first_name(name):
    if name:
        return name.split(" ")[0]


def change_request_color(status):
    if status in config.good_statuses:
        return "green"
    return "grey"


def release_color(issue):
    status = issue["status"]
    if status == config.tested:
        return "green"
    elif status == config.delivered:
        return "grey"
    return "yellow"


def issue_color(sla_text, status):
    if "Overdue" in sla_text:
        color = "red"
    elif "d" not in sla_text:
        color = "yellow"
    elif "Undefined" in sla_text:
        color = "grey"
    elif status == "Open":
        color = "purple"
    else:
        color = "green"
    return color


def issue_emoji(color, priority):
    color = color
    if priority is None:
        return ""
    # fixme: not universal priority codes, not configurable
    if color == "red":
        return "💀"
    elif "1" in priority:
        if color == "yellow":
            return "💔"
        else:
            return "😡"
    elif "2" in priority:
        if color == "yellow":
            return "😰"
        else:
            return "😱"
    elif "4" in priority:
        return "😴"
    elif color == "yellow":
        return "😥"
    return ""


def format_time_tracking(issue):
    original_estimate, remaining_estimate, time_spent = (
        issue["original_estimate"],
        issue["remaining_estimate"],
        issue["time_spent"],
    )
    time_tracking = {
        "estimated": {"time": original_estimate, "reverse": False},
        "remaining": {"time": remaining_estimate, "reverse": True},
        "logged": {"time": time_spent, "reverse": False},
    }

    for bar in time_tracking.values():
        time = bar["time"]
        if time is None:
            bar["time"] = 0
            bar["text"] = "Not Specified"
        else:
            bar["text"] = seconds_to_text(time)

    total_seconds = time_tracking["logged"]["time"] + time_tracking["remaining"]["time"]

    def prepare_bar(seconds, reverse):
        if total_seconds != 0:
            left = int(round(seconds / total_seconds, 2) * 100)
        else:
            left = 0
        right = 100 - left

        if reverse:
            return right, left
        return left, right

    for bar in time_tracking.values():
        bar["left"], bar["right"] = prepare_bar(bar["time"], bar["reverse"])

    return time_tracking


def descriptors(issue, desired):
    return [
        descriptor
        for descriptor in [
            {"label": "Module", "data": issue["module"] or "None"},
            {
                "label": "Assigned to",
                "data": first_name(issue["assignee"]) or "Unassigned 😏",
            },
            {"label": "Issue type", "data": issue["maintenance_type"] or "None"},
            {"label": "Type", "data": issue["issue_type"] or "None"},
            {"label": "Priority", "data": issue["priority"]},
            {"label": "Reporter", "data": first_name(issue["reporter"]) or "No one"},
        ]
        if descriptor["label"] in desired
    ]


def recency(issue):
    creation_date, last_update_date = (
        dateutil.parser.parse(issue["creation_date"]),
        dateutil.parser.parse(issue["last_update_date"]),
    )

    now = datetime.datetime.now(datetime.timezone.utc)

    hours_in_past = 1
    if abs((now - creation_date).total_seconds()) / 3600 < hours_in_past:
        return "NEW"
    elif abs((now - last_update_date).total_seconds()) / 3600 < hours_in_past:
        return "UPDATED"
    return None


def base_issue(issue):
    return {
        "issue": issue["issue"],
        "status": issue["status"],
        "summary": issue["summary"],
        "recent": recency(issue),
    }


def issue_sla(issue):
    try:
        sla = issue["sla"][0]
    except TypeError:
        return "Undefined", 2147483647
    else:
        return parse_sla(sla)


def as_maintenance(issue):
    sla_text, sla_time = issue_sla(issue)

    color = issue_color(sla_text=sla_text, status=issue["status"])
    emoji = issue_emoji(color=color, priority=issue["priority"])

    return dict(
        base_issue(issue),
        **{
            "sla": sla_text,
            "sla_time": sla_time,
            "descriptors": descriptors(
                issue, {"Module", "Assigned to", "Issue type", "Priority"}
            ),
            "color": color,
            "emoji": emoji,
        },
    )


def as_change_request(issue):
    color = change_request_color(status=issue["status"])
    emoji = ""

    return dict(
        base_issue(issue),
        **{
            "developer": first_name(issue["assignee"]),
            "descriptors": descriptors(issue, {"Module", "Reporter"}),
            "time_tracking": format_time_tracking(issue),
            "color": color,
            "emoji": emoji,
        },
    )


def as_tested(issue):
    return dict(
        base_issue(issue),
        **{
            "descriptors": descriptors(
                issue, {"Module", "Reporter", "Assigned to", "Type"}
            ),
            "color": "green",
            "emoji": "",
        },
    )


def as_for_release(issue):
    return dict(
        base_issue(issue),
        **{
            "descriptors": descriptors(
                issue, {"Module", "Reporter", "Assigned to", "Type"}
            ),
            "color": release_color(issue),
            "emoji": "",
        },
    )
