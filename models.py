from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.String(80), unique=True)

    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    def __repr__(self):
        return '<User %r>' % self.username

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tasks = db.Column(db.String(80))
    user_id = db.Column(db.String(80),db.ForeignKey('user.id'))


    def __init__(self, tasks, user_id):
        self.tasks = tasks
        self.user_id = user_id

    def __repr__(self):
        return '<Task %r>' % self.tasks
