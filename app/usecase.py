import base64

from tornado.escape import json_decode, to_unicode, utf8
from sqlalchemy.future import select
from sqlalchemy import delete, text

from model import UserRequest


def get_key_from_body(body: bytes):
    body = json_decode(body)
    res = ''
    for key, value in body.items():
        res += key + str(value)
    return to_unicode(base64.b64encode(utf8(res)))


async def get_by_key(session, key: str):
    async with session() as session:
        row = await session.execute(select(UserRequest).where(UserRequest.key == key))
        user_request = row.scalar()
        return user_request


async def delete_by_key(session, key: str):
    async with session() as session:
        await session.execute(delete(UserRequest).where(UserRequest.key == key))
        await session.commit()


async def create_or_inc_duplicates(session, body: bytes):
    async with session() as session:
        key = get_key_from_body(body)
        row = await session.execute(select(UserRequest).where(UserRequest.key == key))
        user_request = row.scalar()

        if user_request:
            user_request.duplicates += 1
        else:
            user_request = UserRequest(
                key=get_key_from_body(body),
                body=to_unicode(body),
                duplicates=0
            )
            session.add(user_request)
        await session.commit()
        session.refresh(user_request)
        return user_request


async def update_body(session, key, body):
    async with session() as session:
        row = await session.execute(select(UserRequest).where(UserRequest.key == key))
        user_request = row.scalar()
        user_request.body = to_unicode(body)
        user_request.duplicates=0
        user_request.key = get_key_from_body(body)
        await session.commit()
        session.refresh(user_request)
        return user_request


async def percent_of_duplicates (session):
    async with session() as session:
        sql = text('select 100 * sum_duplicates / (obj_count + sum_duplicates) from '
        '(select CAST(sum(duplicates) AS float) as sum_duplicates, CAST(count(*) AS float) as obj_count from '
        'user_request) as foo;'
        )
        row = await session.execute(sql)
        result = row.scalar()
        return result

