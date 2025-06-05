from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from classtalk.models import Question

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_classtalk():
    return 'Hello, Classtalk!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))
