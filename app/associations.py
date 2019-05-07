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

ADMINS = db.Table(
    'admins',
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

USRS = db.Table(
    'usrs',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
        ),
    db.Column(
        'channel_id',
        db.Integer,
        db.ForeignKey('channels.id'),
        primary_key=True
        )
    )
