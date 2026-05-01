from flask import current_app


def get(config_variable):
    return current_app.config.get(config_variable)