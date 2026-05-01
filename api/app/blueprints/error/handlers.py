import re
from flask import Blueprint, request, render_template, redirect, current_app


bp = Blueprint('error', __name__)


def internal_server_error(e):
    current_app.logger.exception(e)

    # add any path to paths_to_ignore in order to ignore errors associated with that path
    # the path can be as general (ie 'static') or as specific (ie 'static/js/map') as desired
    paths_to_ignore = ['']
    do_nothing = False
    pattern = re.compile('(?:https?:\/\/)?(?:www\.)?(?:.*?)\/(.+)')
    this_path = re.findall(pattern, request.url)[0]
    for path in paths_to_ignore:
        if this_path.startswith(path):
            do_nothing = True

    if not do_nothing:
        # send_error_email(e)
        return render_template('error/500.html'), 500


def page_not_found(e):
    current_app.logger.info('Page not found')

    # add any path to paths_to_ignore in order to ignore errors associated with that path
    # the path can be as general (ie 'static') or as specific (ie 'static/js/map') as desired
    paths_to_ignore = []
    do_nothing = False
    pattern = re.compile('(?:https?:\/\/)?(?:www\.)?(?:.*?)\/(.+)')
    this_path = re.findall(pattern, request.url)[0]
    for path in paths_to_ignore:
        if this_path.startswith(path):
            do_nothing = True

    return render_template('error/404.html'), 404
