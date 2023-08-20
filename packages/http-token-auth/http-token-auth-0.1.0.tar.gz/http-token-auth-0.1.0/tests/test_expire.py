# standard imports
import unittest
import time
import logging

# local imports
from http_token_auth.session import Session
from http_token_auth import SessionStore

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class TestSessionExpire(unittest.TestCase):

    auth_delta = 123
    refresh_delta = 456

    def __check_session(self, session, cmp_time):
        self.assertGreater(session.refresh_expire, cmp_time + self.refresh_delta - 1)
        self.assertLess(cmp_time + self.refresh_delta, session.refresh_expire)

        self.assertGreater(session.auth_expire, cmp_time + self.auth_delta - 1)
        self.assertLess(cmp_time + self.auth_delta, session.refresh_expire)


    def test_new(self):
        store = SessionStore()
        k = b'deadbeef'
        session_token = store.new(k)
        s = store.session[k]
        one = store.get(k)
        self.assertIsNotNone(one)


    def test_expire(self):
        t = time.time()
        s = Session('deadbeef', auth_expire_delta=self.auth_delta, refresh_expire_delta=self.refresh_delta)
        self.__check_session(s, t)


    def test_expire_store(self):
        store = SessionStore(auth_expire_delta=self.auth_delta, refresh_expire_delta=self.refresh_delta)
        k = b'deadbeef'
        t = time.time()
        session_token = store.new(k)
        s = store.session[k]
        self.__check_session(s, t)


    def test_renew_expired(self):
        store = SessionStore(auth_expire_delta=0.0000001)
        k = b'deadbeef'
        one = store.new(k)

        s = store.session[k]

        time.sleep(0.0000001)
        two = store.renew(k, store.session[k].refresh)
        self.assertIsNotNone(two)
        self.assertNotEqual(one, two)
        

if __name__ == '__main__':
    unittest.main()
