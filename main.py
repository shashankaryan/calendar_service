import os
import logging

from flask import Flask
from flask_mongoengine import MongoEngine

from logutils import init_logging
from utils import ObjectIDConverter, run, ist_tmz_formatter
from controllers.calendar import calendar_blueprint

# init_logging()
application = Flask(__name__)
application.config.from_envvar('CONFIG_PATH', silent=True)
application.url_map.strict_slashes = False
application.url_map.converters['objectid'] = ObjectIDConverter
application.jinja_env.filters['ist_tmz_formatter'] = ist_tmz_formatter

for i in application.config:
    os.environ[i] = str(application.config[i])
db = MongoEngine(application)

application.register_blueprint(calendar_blueprint)


@application.errorhandler(Exception)
def handle_error(error):
    logging.exception(error)
    return 'Internal Server Error', 503


if __name__ == "__main__":
    run(application)
