from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey


Base = declarative_base()
engine = create_engine('sqlite:///tdiary.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    avatar = Column(String, comment='头像')

    def __repr__(self):
        return "<User(name='%s')>" % self.name


class Diary(Base):
    __tablename__ = 'diary'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    weather = Column(String, comment='天气')
    parent_id = Column(Integer, ForeignKey("diary.id"))
    like = Column(Integer, comment='点赞数')
    creator_id = Column(Integer, ForeignKey("users.id"))

    parent_diary = relationship("Diary", foreign_keys=[parent_id])
    creator = relationship("User", foreign_keys=[creator_id])


if __name__ == '__main__':
    Base.metadata.create_all(engine)
