import tornado
from tornado.escape import to_unicode


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db_session = self.application.db_session

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def write_error(self, status_code, **kwargs):
        self.finish(tornado.escape.json_encode({
            'error': {
                'code': status_code,
                'message': self._reason,
            }
        }))

    def get_required_arguments(self, arg_key):
        arg_value = self.get_arguments(arg_key)
        if not arg_value:
            raise tornado.web.HTTPError(400, reason=f'argument {arg_key} is required')
        return arg_value

    @property
    def body(self):
        return to_unicode(self.request.body)
