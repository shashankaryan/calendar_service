import logging
import json
import datetime

SIMPLE_LOG_FORMAT = {
    "ts": "%(asctime)s",
    "level": "%(levelname)s",
    "location": "%(pathname)s:%(lineno)d",
    "msg": "%(message)s"
}
SIMPLE_DATE_FORMAT = '%d/%b/%Y:%H:%M:%S %Z'


def init_logging():
    log_format = json.dumps(SIMPLE_LOG_FORMAT)
    logging.basicConfig(format=log_format, level=logging.DEBUG, datefmt=SIMPLE_DATE_FORMAT)
    if len(logging.root.handlers) > 0:
        logging.root.handlers[0].setFormatter(
            JsonLogFormatter(fmt=log_format, datefmt=SIMPLE_DATE_FORMAT))


class JsonLogFormatter(logging.Formatter):
    def formatException(self, exc_info):
        stacktrace = super(JsonLogFormatter, self).formatException(exc_info)
        record = {"message": stacktrace, "levelname": "EXCEPTION",
                  "pathname": "stacktrace in msg", "lineno": -1}
        try:
            record['asctime'] = datetime.datetime.now().strftime(SIMPLE_DATE_FORMAT)
            return self._fmt % record
        except Exception as e:
            return repr(stacktrace)
