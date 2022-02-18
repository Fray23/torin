import os

import tornado.ioloop
import tornado.web
import tornado.log
import tornado.locks
import tornado.escape

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from model import Base as models_base
import usecase

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_DATABASE = os.environ.get('POSTGRES_DB')
engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}', echo=True)


class Application(tornado.web.Application):
    def __init__(self, db_session):
        self.db_session = db_session
        handlers = [
            (r'/api/add/', CreateHandler),
            (r'/api/get/', GetHandler),
            (r'/api/update/', UpdateHandler),
            (r'/api/remove/', DeleteHandler),
            (r'/api/statistic', StatisticHandler),
        ]
        settings = dict(
            debug=True,
        )
        super().__init__(handlers, **settings)


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


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(models_base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    app = Application(
        db_session=async_session,
    )
    app.listen(9001)
    shutdown_event = tornado.locks.Event()
    await shutdown_event.wait()

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)
