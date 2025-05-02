from flask_sqlalchemy import SQLAlchemy
from RealProject import db



class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
   

    def __repr__(self):
        return f'<问题 {self.id}: {self.content}>'
    