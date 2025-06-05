from flask import Blueprint, render_template, request, redirect, url_for
from classtalk.models import Question
from classtalk.forms import QuestionForm, AnswerForm
from werkzeug.utils import redirect
from datetime import datetime
# from flask import flash #로그인 관련
# from flask_login import login_required, current_user
from .. import db

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    q_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=q_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    q = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=q, form=form)

@bp.route('/create/', methods=('get', 'post'))
# @login_required  # 로그인한 사용자만 글 작성 가능
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(
            subject=form.subject.data,
            content=form.content.data,
            create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)