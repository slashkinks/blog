from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:48757@localhost/flask_blog'
app.secret_key = 'shh'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    roles = db.relationship('Role', backref='user', lazy='dynamic')

    def __int__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, role, user_id):
        self.role=role
        self.user_id = user_id

    def __repr__(self):
        return '<Role %r>' % self.role


tags = db.Table('tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable=False),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), nullable=False),
    db.PrimaryKeyConstraint('post_id', 'tag_id'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    published = db.Column(db.Boolean)
    published_date = db.Column(db.Date)
    last_edit_date = db.Column(db.Date)
    tags = db.relationship('Tag', secondary=tags, backref='post')#, backref=db.backref('post', lazy='dynamic'))

    def __init__(self, title, body, published):
        self.title = title
        self.body = body
        self.published_date = datetime.utcnow()
        self.published = published
        self.last_edit_date = datetime.utcnow()


    def _find_tag(self, tag):
        q = Tag.query.filter_by(tag_name=tag)
        return q.first()

    def _get_tags(self):
        return [x.tag_name for x in self.tags]

    def _set_tags(self, value):
        for tag in value:
            self.tags.append(self._find_tag(tag))

    @staticmethod
    def make_description(body_of_post):
        res = ''
        sep = '</p>'
        paragraphs = body_of_post.split(sep)

        for paragraph in paragraphs:
            res = paragraph
            break
        return res

    def __repr__(self):
        return '<Post %r>' % self.title


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.tag_name = name

    def __repr__(self):
        return '<Tag_name %r>' % self.tag_name

