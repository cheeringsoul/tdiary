import redis

from model import open_db_session, User


def init():
    r = redis.Redis(host='localhost', port=6379, db=0)
    pipe = r.pipeline()

    with open_db_session() as session:
        rv = session.query(User).all()
        for each in rv:
            pipe.set(f"user.{each.id}", each.avatar)
            pipe.execute()

    r.close()
