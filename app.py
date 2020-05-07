from datetime import timedelta
from logging.config import dictConfig
from flask import Flask, render_template, current_app, flash
from werkzeug.utils import find_modules, import_string
from common.context import load_current_user

from ext import csrf


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'tdiary': {
        'class': 'logging.FileHandler',
        'filename': 'tdiary-log.log',
        'mode': 'w',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['tdiary']
    }
})


def page_not_found(e):
    return render_template('404.html'), 404


def inter_error(e):
    current_app.logger.error(e)
    flash("服务器内部错误!!")
    return render_template('message.html')


class Application(Flask):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(__name__, *args, **kwargs)
        self.url_map.strict_slashes = False
        self.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        self.permanent_session_lifetime = timedelta(days=7)
        csrf.init_app(self)
        self.before_request(load_current_user)
        self.register_error_handler(404, page_not_found)
        self.register_error_handler(500, inter_error)

    def register_blueprints(self, root):
        for name in find_modules(root, recursive=True):
            mod = import_string(name)
            if hasattr(mod, 'bp'):
                self.register_blueprint(mod.bp)


def date(datetime):
    return datetime.strftime('%Y-%m-%d')


def create_app(*args, **kwargs):
    app = Application(*args, **kwargs)
    app.register_blueprints('view')
    app.jinja_env.filters['date'] = date
    return app


application = create_app()


if __name__ == '__main__':
    application.run("0.0.0.0", 80, debug=True)
