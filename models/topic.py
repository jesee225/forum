from utils import format_time
from . import ReprMixin
from . import db


class Topic(db.Model, ReprMixin):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    content = db.Column(db.Text())
    created_time = db.Column(db.Integer, default=format_time())
    updated_time = db.Column(db.Integer, default=format_time())

    comments = db.relationship('Comment', backref='topic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, form):
        print('topic init', form)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.created_time = format_time()

    def _update(self, form):
        print('topic update', form)
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.updated_time = format_time()
        self.save()


class Comment(db.Model, ReprMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    created_time = db.Column(db.Integer, default=format_time())
    updated_time = db.Column(db.Integer, default=format_time())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))

    def __init__(self, form):
        print('comment init', form)
        self.topic_id = form.get('topic_id', '')
        self.content = form.get('content', '')
        self.created_time = format_time()
