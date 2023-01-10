from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from ApplePie import db
from ApplePie.forms import UserCreateForm, UserLoginForm
from ApplePie.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 회원가입 함수
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    
    # forms.py UserCreateForm() 함수 사용
    form = UserCreateForm()

    if request.method == 'POST' and form.validate_on_submit():
        
        # 데이터베이스 id 중복 확인 진행
        user = User.query.filter_by(username=form.username.data).first()

        # user가 존재하지 않는 경우
        if not user:
            user = User(nickname=form.nickname.data,
                        username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        )
            # 데이터베이스 정보 저장
            db.session.add(user)
            db.session.commit()

            # main_views.py index() 함수 실행
            return redirect(url_for('main.index'))
        
        # id가 중복 된다면
        else:
            flash('이미 존재하는 사용자입니다.')
    
    # 처음 sign_up 버튼 클릭시
    return render_template('auth/sign_up.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        # user가 데이터베이스에 존재하는지 여부 확인
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        # user가 존재하면 비밀번호 확인
        # 비밀번호가 일치하지 않을 경우
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        
        # error가 None이라면
        if error is None:
            session.clear()
            session['user_id'] = user.id
            # main_views.py index() 함수 실행
            return redirect(url_for('main.index'))
        flash(error)

    # login 페이지 호출
    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))