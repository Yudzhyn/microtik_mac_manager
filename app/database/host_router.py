# db
from . import db


class HostRouter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    ip = db.Column(db.String(30), unique=False, nullable=False)
    port = db.Column(db.Integer, unique=False, nullable=False, default=22000)

    host_group_id = db.Column(db.Integer, db.ForeignKey('host_group.id'), nullable=False)
    host_group = db.relationship('HostGroup', backref=db.backref('host_routers', lazy=True))

    def __repr__(self):
        return "<HostRouter name='{}' ip='{}' port='{}' group='{}'>" \
            .format(self.name, self.ip, self.port, self.host_group)
