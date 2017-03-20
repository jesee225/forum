from models.topic import Topic
from models.topic import Comment
from routes import *

main = Blueprint('topic', __name__)

Model = Topic


@main.route('/')
def index():
    u = current_user()
    ms = Model.query.all()
    return render_template('topic/index.html', topics=ms, user=u)


@main.route('/user/<int:id>')
def user_index(id):
    u = current_user()
    ms = Model.query.filter_by(user_id=id).all()
    return render_template('topic/user_index.html', topics=ms, user=u)


@main.route('/<int:id>')
def detail(id):
    u = current_user()
    m = Model.query.get(id)
    cs = m.comments
    return render_template('topic/detail.html', topic=m, comments=cs, user=u)


@main.route('/new')
@login_required
def new():
    u = current_user()
    return render_template('topic/new.html', user=u)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Model(form)
    u = current_user()
    m.user_id = u.id
    m.save()
    return redirect(url_for('topic.detail', id=m.id))


@main.route('/edit/<int:id>')
@login_required
def edit(id):
    u = current_user()
    m = Model.query.get(id)
    if m.user_id == u.id:
        return render_template('topic/edit.html', topic=m, user=u)
    else:
        return redirect(url_for('topic.detail', id=id))


@main.route('/update/<int:id>', methods=['POST'])
def update(id):
    form = request.form
    Model.update(id, form)
    return redirect(url_for('topic.detail', id=id))


@main.route('/comment', methods=['POST'])
@login_required
def comments():
    form = request.form
    c = Comment(form)
    u = current_user()
    c.user_id = u.id
    c.save()
    return redirect(url_for('topic.detail', id=c.topic_id))
