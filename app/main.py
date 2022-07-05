import tornado.ioloop
import tornado.web
import tornado.log
import tornado.locks
import tornado.escape

from db import sqlalchemy_engine, async_session
from model import Base as models_base
from api.urls import urls

from settings import DEBUG, COOKIE_SECRET, TORNADO_AUTORELOAD


def get_prefixed(url, url_prefix):
    return url_prefix + url[0], url[1]


class Application(tornado.web.Application):
    def __init__(self, db_session):
        self.db_session = db_session
        handlers = urls
        settings = dict(
            debug=DEBUG,
            cookie_secret=COOKIE_SECRET,
            autoreload=TORNADO_AUTORELOAD
        )
        super().__init__(handlers, **settings)


async def main():
    async with sqlalchemy_engine.begin() as conn:
        await conn.run_sync(models_base.metadata.create_all)

    app = Application(
        db_session=async_session,
    )
    app.listen(9001)
    shutdown_event = tornado.locks.Event()
    await shutdown_event.wait()

if __name__ == "__main__":
    tornado.ioloop.IOLoop.current().run_sync(main)
