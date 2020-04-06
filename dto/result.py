import json


class ResponseDto:
    """
    :arg status 0 means success and -1 means failure
    :arg result should be json
    :arg msg message
    """

    def __init__(self, status=0, result=None, msg=""):
        if result is None:
            result = {}
        self.status = status
        self.result = result
        self.msg = msg

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
