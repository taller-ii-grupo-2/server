"""Here we set the associations in many to many relations"""
from app import db


ORGS = db.Table(
    'orgs',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
        ),
    db.Column(
        'organization_id',
        db.Integer,
        db.ForeignKey('organizations.id'),
        primary_key=True
        )
    )
