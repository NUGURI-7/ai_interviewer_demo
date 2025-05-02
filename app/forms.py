from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired



class QuestionForm(FlaskForm):
    content = TextAreaField('问题内容', validators=[DataRequired(message='内容不能为空哦！')])
    submit = SubmitField('提交')