from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = None
session_factory = sessionmaker()
Session = scoped_session(session_factory)


def bind_session_engine(*args, **kwargs):
    global engine, session_factory, Session
    engine = create_engine(*args, **kwargs)
    Session.remove()
    session_factory.configure(bind=engine)
    return engine
