from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()


class UserRequest(Base):
    __tablename__ = 'user_request'
    id = Column(Integer, primary_key=True)
    key = Column(String(512), unique=True)
    body = Column(Text)
    duplicates = Column(Integer, default=0)

    def __repr__(self):
        return f'<UserRequest id={self.id}, key={self.key}>'
