import unittest

import db
from db import bind_session_engine, Session


class DBTestCase(unittest.TestCase):

    def tearDown(self):
        Session.remove()


class BindSessionEngineTest(DBTestCase):

    def test_overwrites_default_session_engine(self):
        bind_session_engine("sqlite://")
        self.assertEqual(db.engine.name, "sqlite")
        self.assertEqual(db.engine.url.host, None)
        self.assertEqual(Session().bind.engine.name, "sqlite")
        self.assertEqual(Session().bind.engine.url.host, None)


class SessionIsScopedTest(DBTestCase):

    def test_request_always_uses_same_session(self):
        s1 = Session()
        s2 = Session()
        self.assertEqual(s1, s2)

    def test_multiple_requests_do_not_share_same_session(self):
        s1 = Session()
        # Simulate a new request creating a new thread, and hence a new session
        Session.remove()
        s2 = Session()
        self.assertNotEqual(s1, s2)
