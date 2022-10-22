# db
from . import db


class HostGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return "<HostGroup name='{}'>".format(self.name)
