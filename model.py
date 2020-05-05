from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey


Base = declarative_base()
engine = create_engine('mysql+pymysql://root:12345678@localhost/diary')
Session = sessionmaker(bind=engine)


@contextmanager
def open_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


class Validated(object):
    Yes = 1
    No = 0


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), unique=True)
    password = Column(String(128))
    email = Column(String(50), unique=True)
    avatar = Column(String(50), comment='头像')
    validated = Column(Integer, comment='是否已经验证过邮箱')

    def __repr__(self):
        return "<User(name='%s')>" % self.name


class DiaryType(object):
    NewDiary = 1
    RewriteDiary = 2
    ContinueDiary = 3


class Diary(Base):
    __tablename__ = 'diary'

    id = Column(Integer, primary_key=True)
    content = Column(String(800))
    weather = Column(String(5), comment='天气')
    diary_type = Column(Integer, comment='日记类型 1新日记，2改写，3续写')
    parent_id = Column(Integer, ForeignKey("diary.id"))
    like = Column(Integer, comment='点赞数', default=0)
    creator_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    parent_diary = relationship("Diary", foreign_keys=[parent_id])
    creator = relationship("User", foreign_keys=[creator_id])


if __name__ == '__main__':
    Base.metadata.create_all(engine)
