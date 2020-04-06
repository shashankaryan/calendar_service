import pytz
import optparse
from flask import request
from tzlocal import get_localzone
from bson.errors import InvalidId
from bson.objectid import ObjectId
from werkzeug.routing import BaseConverter, ValidationError


class ObjectIDConverter(BaseConverter):
    def to_python(self, value):
        try:
            return ObjectId(value)
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return value


def run(app, default_host="127.0.0.1", default_port="8000"):
    """ Takes a flask.Flask instance and runs it.
    Parses command-line flags to configure the app."""

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host", help="Hostname of the Flask app [default {}]".format(default_host),
                      default=default_host)
    parser.add_option("-P", "--port", help="Port for the Flask app [default {}]".format(default_port),
                      default=default_port)
    # Two options useful for debugging purposes, but 
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile", action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
        options.debug = True
    app.run(debug=options.debug, host=options.host, port=int(options.port))


def get_page_items():
    """ calculate offset according to page number """
    page = int(request.args.get('pageNumber', 1))
    per_page = int(request.args.get('pageSize', 100))
    offset = (page - 1) * per_page
    return page, per_page, offset


def ist_tmz_formatter(value, time_format="%Y-%m-%d %H:%M"):
    if value:
        to_tz = pytz.timezone('Asia/Kolkata')   # timezone you want to convert to from local
        local_tz = get_localzone()
        value = local_tz.localize(value, is_dst=None).astimezone(pytz.utc)
        new_tz_dt = value.astimezone(to_tz)
        return new_tz_dt.strftime(time_format)
    else:
        return ''
