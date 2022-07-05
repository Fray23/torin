import tornado.ioloop
import tornado.web
import tornado.log
import tornado.locks
import tornado.escape

import usecase
from api.deps import BaseHandler


class CreateHandler(BaseHandler):
    async def post(self):
        user_request = await usecase.create_or_inc_duplicates(self.db_session, self.request.body)
        self.write({
            'key': user_request.key
        })


class UpdateHandler(BaseHandler):
    async def put(self):
        key = self.get_required_arguments('key')
        user_re = await usecase.update_body(self.db_session, key[0], self.request.body)
        self.write({
            'key': user_re.key
        })


class GetHandler(BaseHandler):
    async def get(self):
        key = self.get_required_arguments('key')
        user_request = await usecase.get_by_key(self.db_session, key[0])
        if user_request:
            self.write({
                'body': tornado.escape.json_decode(user_request.body),
                'duplicates': user_request.duplicates
            })
        else:
            raise tornado.web.HTTPError(404, reason='Not found')


class DeleteHandler(BaseHandler):
    async def delete(self):
        key = self.get_required_arguments('key')
        await usecase.delete_by_key(self.db_session, key[0])
        self.set_status(204)
        await self.finish()


class StatisticHandler(BaseHandler):
    async def get(self):
        percent = await usecase.percent_of_duplicates(self.db_session)
        if percent:
            self.write({
                'percent_of_duplicates': percent
            })