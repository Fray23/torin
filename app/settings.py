import os

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_DATABASE = os.environ.get('POSTGRES_DB')

database_url = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}'

DEBUG = True
COOKIE_SECRET = ']Q~JKSVY<N},CC}]2@EQ0shY1:zycfcOhvRB%{tj`2e$ynHH`(0=o;}yABc8Q]x(}%svC}W&1wFrVaHP4PxPGWySN'
TORNADO_AUTORELOAD = True
