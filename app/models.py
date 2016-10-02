from . import db

class Role(object):

    pass


class User(object):
    pass


class Entry(db.Model):
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1
    STATUS_DELETED = 2

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)

    def  __init__(self, title=None, body=None, status=None):

        self.title = title
        self.body= body
        self.status = status


    def __repr__(self):


        return  '<Entry {0}>'.format(self.title)

