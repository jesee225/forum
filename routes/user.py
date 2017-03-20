
from routes import *

main = Blueprint('user', __name__)

Model = User


@main.route('/login', methods=['GET', 'POST'])
def login():
    method = request.method
    if method == 'GET':
        return render_template('user/login.html')
    else:
        form = request.form
        username = form.get('username', '')
        # 检查 user 是否存在于数据库中并且验证登录的用户名和密码是否正确
        model = Model.query.filter_by(username=username).first()
        print(username)
        if model is not None and model.validate_auth(form):
            print('登录成功')
            session['user_id'] = model.id
            return redirect(url_for('topic.index'))
        else:
            print('登录失败')
            # url_for(蓝图名.路由函数）
            return redirect(url_for('user.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    method = request.method
    if method == 'GET':
        print('get')
        return render_template('user/register.html')
    else:
        form = request.form
        m = Model(form)
        # 检查 user 是否存在于数据库中并且验证注册的用户名和密码是否正确
        if m.valid():
            print('注册成功')
            m.save()
            session['user_id'] = m.id
            return redirect(url_for('topic.index'))
        else:
            print('注册失败')
            return redirect(url_for('user.register'))


@main.route('/profile')
@login_required
def profile():
    u = current_user()
    number_of_topics = len(u.topics)
    number_of_comments = len(u.comments)
    return render_template('user/profile.html', user=u, number_of_topics=number_of_topics,
                           number_of_comments=number_of_comments)


@main.route('/profile/<int:id>')
@login_required
def user_profile(id):
    m = Model.query.get(id)
    number_of_topics = len(m.topics)
    number_of_comments = len(m.comments)
    return render_template('user/user_profile.html', owner=m, number_of_topics=number_of_topics,
                           number_of_comments=number_of_comments)
