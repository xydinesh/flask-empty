# -*- coding:utf-8 -*-

import os
import sys
from empty import Empty

{%- if cookiecutter.create_index != 'no' %}
from flask import render_template
{% endif %}

# apps is a special folder where you can place your blueprints
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_PATH, "apps"))

basestring = getattr(__builtins__, 'basestring', str)


class App(Empty):
    {% if cookiecutter.use_sql == 'yes' %}
    def configure_database(self):
        "Database configuration should be set here"
        from database import db

        db.app = self
        db.init_app(self)
    {%- endif %}
    {% if cookiecutter.create_index != 'no' %}
    def configure_views(self):
        @self.route('/')
        def index_view():
            return render_template("index.html")
    {% else %}
    def configure_views(self):
        pass
    {%- endif %}

def config_str_to_obj(cfg):
    if isinstance(cfg, basestring):
        module = __import__('config', fromlist=[cfg])
        return getattr(module, cfg)
    return cfg


def app_factory(config, app_name, blueprints=None):
    # you can use Empty directly if you wish
    app = App(app_name)
    config = config_str_to_obj(config)

    app.configure(config)
    app.add_blueprint_list(blueprints or config.BLUEPRINTS)
    app.setup()

    return app


def heroku():
    from config import Config, project_name
    # setup app through APP_CONFIG envvar
    return app_factory(Config, project_name)