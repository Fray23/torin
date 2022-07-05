from api.handlers.user_request import *


urls = [
    (r'/api/add', CreateHandler),
    (r'/api/get', GetHandler),
    (r'/api/update', UpdateHandler),
    (r'/api/remove', DeleteHandler),
    (r'/api/statistic', StatisticHandler),
]
