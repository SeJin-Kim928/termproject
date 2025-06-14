from flask import Blueprint, render_template, request, redirect, url_for, g, flash
from wtforms.validators import none_of
from classtalk.models import Question, Answer, User
from classtalk.forms import QuestionForm, AnswerForm
from werkzeug.utils import redirect
from datetime import datetime
from classtalk import db
from classtalk.views.auth_views import login_required

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    q = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=q, form=form)

@bp.route('/create/', methods=('get', 'post'))
@login_required  # 로그인한 사용자만 글 작성 가능
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(
            subject=form.subject.data,
            content=form.content.data,
            is_anonymous=form.is_anonymous.data,  # 익명 여부 저장
            user_id=None if form.is_anonymous.data else g.user.id,  # 익명 처리
            create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        flash('답변이 등록되었습니다!', 'success')
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정 권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

@bp.route('/answer/delete/<int:answer_id>/')
@login_required
def answer_delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)

    if g.user != answer.user:
        flash('답변 삭제 권한이 없습니다.', 'danger')
        return redirect(url_for('question.detail', question_id=answer.question_id))

    question_id = answer.question_id  # 삭제 후 질문 상세 페이지로 돌아가기 위해 미리 저장
    db.session.delete(answer)
    db.session.commit()

    flash('답변이 삭제되었습니다.', 'success')
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/answer/create/<int:question_id>/', methods=('POST',))
@login_required
def answer_create(question_id):
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(
            question_id=question_id,
            content=form.content.data,
            is_anonymous=bool(form.is_anonymous.data),  # ✅ 익명 여부 저장
            user_id=None if form.is_anonymous.data else g.user.id,  # ✅ 익명 처리 (문제 발생)
            create_date=datetime.now(), user=g.user

        )
    db.session.add(answer)
    db.session.commit()
    flash('답변이 등록되었습니다!', 'success')
    return redirect(url_for('question.detail', question_id=question_id))
