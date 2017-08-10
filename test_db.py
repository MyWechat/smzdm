import unittest
import os
from db import Storage


class DbTestCase(unittest.TestCase):
    DB_NAME = 'test.db'
    PUSH_DATA = {'foo': 'bar'}

    def tearDown(self):
        os.remove(self.DB_NAME)

    def setUp(self):
        self.s = Storage(self.DB_NAME)

    def testInit(self):
        self.assertTrue(os.path.isfile(self.DB_NAME))

    def testPush(self):
        id = self.s.add_push(self.PUSH_DATA)
        self.assertDictEqual(self.s.pushed(str(id)), self.PUSH_DATA)

    def testFlush(self):
        self.s.flush_push()


if __name__ == '__main__':
    unittest.main()
