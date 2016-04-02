import unittest
from app.master import start
class TestMaster(unittest.TestCase):

    def test_master_accepts_connections_from_nodes(self):
        thread.start_new_thread(start,(1200,'master'))
        thread.start_new_thread(start,(1200,'master'))
