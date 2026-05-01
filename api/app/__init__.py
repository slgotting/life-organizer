import os
import time
import re
import traceback
import stripe
from flask_mail import Mail
from flask import Flask, request, render_template
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l
from flask_migrate import Migrate
from logger_slg import init_logger

from config import config
from flask_login import current_user, LoginManager, login_user


login_manager = LoginManager()
login_manager.login_view = "admin.login"

cors = CORS(
    origins=['*']
    #     'www.%%APP_DOMAIN%%',
    #     '%%APP_DOMAIN%%',
    #     'staging.%%APP_DOMAIN%%',
    #     'https://staging.%%APP_DOMAIN%%',
    #     'http://staging.%%APP_DOMAIN%%',
    #     'https://www.%%APP_DOMAIN%%',
    #     'http://www.%%APP_DOMAIN%%',
    #     'https://%%APP_DOMAIN%%',
    #     'http://%%APP_DOMAIN%%',
    #     'https://staging.tennis-lines.com',
    #     'http://staging.tennis-lines.com',
    #     'https://tennis-lines.com',
    #     'http://tennis-lines.com',
    #     'http://127.0.0.1:5173'
    # ]
)
mail = Mail()
mongo_db = MongoEngine()
sql_db = SQLAlchemy()
bootstrap = Bootstrap()
babel = Babel()
migrate = Migrate()

def create_app(config_name='default'):
    print(f'\nconfig_name:\n {config_name}\n', flush=True)
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    login_manager.init_app(app)
    cors.init_app(app)
    mongo_db.init_app(app)
    sql_db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, sql_db)

    app.logger = init_logger(
        log_path='./app.log',
    )

    # im still not sure why this is needed. The production config for some reason wasn't properly setting these config variables
    app.config.update(
        STRIPE_SECRET_KEY=os.environ.get("STRIPE_SECRET_KEY", app.config.get("STRIPE_SECRET_KEY")),
        STRIPE_WEBHOOK_SECRET=os.environ.get("STRIPE_WEBHOOK_SECRET", app.config.get("STRIPE_WEBHOOK_SECRET")),
    )

    stripe.api_key = app.config.get("STRIPE_SECRET_KEY")

    from app.blueprints.mongo.api_token_auth.models import BlacklistToken

    # create dummy blacklist token if one doesnt exist
    if not BlacklistToken.objects.first():
        BlacklistToken(token="dummy").save()

    # HOW TO ADD THIS WITH TOKEN AUTH? SEEMS LIKE THIS STRIPS HEADERS FROM THE REQUEST
    # @app.before_request
    # def ping_user():
    #     from app.blueprints.sql.api_token_auth.helpers import get_user_from_request_headers
    #     user = get_user_from_request_headers(request.headers)
    #     user.ping()

    @app.before_request
    def snoozer():
        time.sleep(0.25)

    app.request_count = 0
    @app.before_request
    def track_total_requests():
        app.request_count += 1

    from app.blueprints.sql.admin.models import Admin
    @login_manager.user_loader
    def load_user(user_id):
        try:
            user = sql_db.one_or_404(sql_db.select(Admin).filter_by(id=user_id))
            if user:
                return user
        except Exception as e:
            pass

    # @app.errorhandler(500)
    # def internal_error(error):
    #     sql_db.session.rollback()
    #     return render_template('500.html'), 500

    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.email import bp as email_bp
    app.register_blueprint(email_bp)

    # from app.blueprints.referral import bp as referral_bp
    # app.register_blueprint(referral_bp)

    from app.blueprints.mongo.api_token_auth import bp as token_bp
    app.register_blueprint(token_bp)

    from app.blueprints.settings import bp as settings_bp
    app.register_blueprint(settings_bp)

    # from app.blueprints.sql.api_token_auth import bp as token_bp
    # app.register_blueprint(token_bp)

    from app.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    # from app.blueprints.subscription import bp as subscription_bp
    # app.register_blueprint(subscription_bp)

    # from app.blueprints.payments_stripe import bp as stripe_bp
    # app.register_blueprint(stripe_bp)

    # from app.blueprints.ai import bp as ai_bp
    # app.register_blueprint(ai_bp)

    # from app.blueprints.sql.admin import bp as admin_bp
    # app.register_blueprint(admin_bp)

    from app.blueprints.error import bp as error_bp
    app.register_blueprint(error_bp)

    @app.errorhandler(Exception)
    def internal_server_error(e):
        from app.blueprints.email.email import send_email
        app.logger.exception(e)

        # add any path to paths_to_ignore in order to ignore errors associated with that path
        # the path can be as general (ie 'static') or as specific (ie 'static/js/map') as desired
        paths_to_ignore = []
        do_nothing = False
        pattern = re.compile('(?:https?:\/\/)?(?:www\.)?(?:.*?)\/(.+)')
        this_path = re.findall(pattern, request.url)[0]
        for path in paths_to_ignore:
            if this_path.startswith(path):
                do_nothing = True

        if not do_nothing:
            try:
                # send_email('Error', ('schedule-it.io', 'admin@schedule-it.io'), ['mail@slgotting.com'], text_body=f'Error: \n\n{traceback.format_exc()}')
                pass
            except:
                pass
            return render_template('error/500.html'), 500

    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.info('Page not found')

        # add any path to paths_to_ignore in order to ignore errors associated with that path
        # the path can be as general (ie 'static') or as specific (ie 'static/js/map') as desired
        paths_to_ignore = []
        do_nothing = False
        pattern = re.compile('(?:https?:\/\/)?(?:www\.)?(?:.*?)\/(.+)')
        this_path = re.findall(pattern, request.url)[0]
        for path in paths_to_ignore:
            if this_path.startswith(path):
                do_nothing = True

        if not do_nothing:
            return render_template('error/404.html'), 404

    return app