from datetime import timedelta
from flask import Flask, render_template
from werkzeug.utils import find_modules, import_string

from common.context import load_current_user
from ext import csrf


def page_not_found(e):
    return render_template('404.html'), 404


class Application(Flask):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(__name__, *args, **kwargs)
        self.url_map.strict_slashes = False
        self.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        self.permanent_session_lifetime = timedelta(days=7)
        csrf.init_app(self)
        self.before_request(load_current_user)
        self.register_error_handler(404, page_not_found)

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
