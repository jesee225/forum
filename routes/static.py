from routes import *

main = Blueprint('static', __name__)


@main.route('/')
def index():
    return redirect(url_for('topic.index'))
