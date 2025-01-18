from db import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)  # Alterado para 'title'

    def __repr__(self):
        return f'<Task {self.title}>'
