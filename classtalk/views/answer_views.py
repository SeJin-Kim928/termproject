from flask import Blueprint, render_template, request, redirect, url_for, g

from classtalk.models import Question, Answer
from datetime import datetime
from classtalk import db
from classtalk.forms import AnswerForm
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>/', methods = ['POST'])
@login_required #로그인 한 사용자만 사용 가능
def create(question_id):
    form = AnswerForm()
    if form.validate_on_submit():
        question = Question.query.get_or_404(question_id)
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question_id=question_id, form=form)