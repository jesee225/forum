from utils import format_time
from . import ReprMixin
from . import db


class User(db.Model, ReprMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text())
    password = db.Column(db.Text())
    img = db.Column(db.Text(), default='/uploads/default.png')
    created_time = db.Column(db.Integer, default=format_time())

    topics = db.relationship('Topic', backref='user')
    comments = db.relationship('Comment', backref='user')

    def __init__(self, form):
        super(User, self).__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = format_time()

    def validate_auth(self, form):
        username = form.get('username', '')
        password = form.get('password', '')
        username_equals = self.username == username
        password_equals = self.password == password
        return username_equals and password_equals

    def _update(self, form):
        print('user.update, ', form)
        self.password = form.get('password', self.password)

    def find_username(self):
        return User.query.filter_by(username=self.username).first()

    def valid(self):
        username_len = len(self.username) >= 3
        password_len = len(self.password) >= 3
        if self.find_username() is None:
            return username_len and password_len

