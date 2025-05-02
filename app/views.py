from flask import (render_template, request, Blueprint, 
                   url_for, redirect, flash, jsonify)
from RealProject import db
from app.models import Question
from app.forms import QuestionForm



bp = Blueprint('ai', __name__, url_prefix='/ai', 
               template_folder='templates', static_folder='static')


@bp.route('/')
def index():
    
    return render_template('chat.html')


@bp.route('/commit', methods=['GET', 'POST'])

def commit_page():
    form = QuestionForm()

    if form.validate_on_submit():
        new_question = Question(content=form.content.data.strip())
        db.session.add(new_question)
        db.session.commit()
        flash('问题提交成功！', 'success')
        return redirect(url_for('ai.commit_page'))

    # 获取所有题目
    questions = Question.query.order_by(Question.id.desc()).all()

    return render_template('commit.html', form=form, questions=questions)

  









    return render_template('commit.html')







