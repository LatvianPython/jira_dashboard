import datetime
import itertools
import operator
import os

from flask import Flask, jsonify, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import config
from authentication import jwt, bcrypt, jwt_required, current_identity
from issues import as_change_request, as_maintenance, as_tested, as_for_release
from jira_integration import jira_issues, jira_dumper
from models import db, Sprint

app = Flask(__name__)

with open(os.environ["FLASK_SECRET_FILE"], mode="rb") as secret_file:
    app.config["SECRET_KEY"] = secret_file.read()

app.config["JWT_AUTH_URL_RULE"] = "/api/auth"
app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(weeks=1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"

bcrypt.init_app(app)
jwt.init_app(app)
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


def issues(formatter, jira_filter):
    return jsonify(
        {
            "issues": [
                formatter(issue) for issue in jira_issues(jql=f"filter = {jira_filter}")
            ]
        }
    )


@app.route("/api/sprint", methods=["GET", "POST"])
@jwt_required()
def sprint_api():
    if not current_identity.is_admin:
        return "Only admin can edit/view", 403

    if request.method == "POST":
        if request.is_json:
            sprint = request.get_json()
            Sprint.query.delete()

            for index, issue in enumerate(sprint, 1):
                issue["id"] = index
                db.session.add(Sprint(**issue))

            db.session.commit()

        else:
            return "Request was not JSON", 400

    return jsonify(
        [
            {
                "id": issue.id,
                "issue": issue.issue,
                "developer": issue.developer,
                "priority": issue.priority,
            }
            for issue in Sprint.query.all()
        ]
    )


def smart_formatter(issue):
    if issue["issue_type"] == "Issue":
        return as_maintenance(issue)
    return as_change_request(issue)


@app.route("/api/favorite_filters")
@jwt_required()
def favorite_filters():
    return jsonify(
        [
            {"filter_id": favorite_filter.filter_id, "name": favorite_filter.name}
            for favorite_filter in current_identity.favorite_filters
        ]
    )


@app.route("/api/generic/<int:filter_id>")
@jwt_required()
def generic(filter_id):
    return issues(smart_formatter, filter_id)


@app.route("/api/filters")
@jwt_required()
def filters():
    return jsonify(
        [
            {"item": favorite_filter.id, "name": favorite_filter.name}
            for favorite_filter in jira_dumper.jira.favourite_filters()
        ]
    )


@app.route("/api/maintenance")
@jwt_required()
def maintenance():
    return issues(as_maintenance, config.jira_maintenance_filter_id)


@app.route("/api/tested")
@jwt_required()
def tested():
    return issues(as_tested, config.jira_tested_filter_id)


@app.route("/api/fix_versions")
@jwt_required()
def fix_versions():
    unreleased = list(jira_dumper.unreleased_project_versions(config.project_key))

    data = list(jira_issues(jql=f"filter = {config.jira_fix_version_filter_id}"))

    by_release = {
        release.id: {"release": release.raw, "issues": []} for release in unreleased
    }

    for release in unreleased:
        for issue in data:
            if release.id in [release["id"] for release in issue["fix_versions"]]:
                by_release[release.id]["issues"].append(as_for_release(issue))

    by_release = [
        {
            "issues": release["issues"],
            "description": release["release"]["description"],
            "name": release["release"]["name"],
            "id": release["release"]["id"],
        }
        for release in by_release.values()
        if release["issues"]
    ]

    return jsonify(by_release)


@app.route("/api/change_requests")
@jwt_required()
def change_requests():
    sprint = Sprint.query.all()

    jql = f"""
    project = "{config.project}" 
AND issuekey in ({",".join(map(operator.attrgetter("issue"), sprint))})"""

    data = list(map(as_change_request, jira_issues(jql=jql)))

    data = {issue["issue"]: issue for issue in data}

    for ticket in sprint:
        data[ticket.issue]["developer"] = ticket.developer
        data[ticket.issue]["priority"] = ticket.priority

    def key(issue):
        return issue["developer"]

    sorted_input = sorted(data.values(), key=key)
    groups = itertools.groupby(sorted_input, key=key)
    by_developer = [
        {"developer": k, "change_requests": [x for x in v]} for k, v in groups
    ]

    return jsonify(by_developer)


if __name__ == "__main__":
    manager.run()
