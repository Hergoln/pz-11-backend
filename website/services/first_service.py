from flask import render_template, Blueprint

basic_bp = Blueprint("basic", __name__)

@basic_bp.route('/hello/')
@basic_bp.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
