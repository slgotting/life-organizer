from app import mongo_db as db
import datetime
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash, current_app
from app.blueprints.mongo.admin import bp
from app.blueprints.mongo.admin.models import Admin
from app.blueprints.mongo.admin.route_protection import admin_required
from app.blueprints.mongo.admin.forms import LoginForm
from app.blueprints.mongo.admin.helpers import get_form_model_attributes

@bp.route("/")
def index():
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    return render_template('admin/index.html', links=links)

@bp.route('/not_authorized')
def not_authorized():
    return render_template('admin/not_authorized.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user._cls == "Admin":
        return redirect(url_for('admin.index'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.objects(username=form.username.data).first()
        if admin is None or not check_password_hash(admin.password_hash, form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('admin.login'))
        logout_user() # we have to call this here because we are logged in by default as an unregistered user
        login_user(admin, remember=True, duration=datetime.timedelta(days=30))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('admin/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
