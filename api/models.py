from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, db.Sequence("user_id_seq"), primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(60))
    is_admin = db.Column(db.Boolean, nullable=False)
    favorite_filters = db.relationship("FavoriteFilter")


class Sprint(db.Model):
    id = db.Column(db.Integer, db.Sequence("sprint_id_seq"), primary_key=True)
    issue = db.Column(db.String(10))
    developer = db.Column(db.String(50))
    priority = db.Column(db.Integer)


class FavoriteFilter(db.Model):
    id = db.Column(db.Integer, db.Sequence("favorite_filter_id_seq"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    filter_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
