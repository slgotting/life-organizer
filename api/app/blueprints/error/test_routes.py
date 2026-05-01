from flask import render_template

from app.blueprints.error import bp

@bp.route('/404')
def test_404():
    return render_template('error/404.html')

@bp.route('/500')
def test_500():
    return render_template('error/500.html')

@bp.route('error')
def error():
    x = 1/0
    return render_template('error/500.html')
