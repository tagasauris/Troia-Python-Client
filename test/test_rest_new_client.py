# -*- coding: utf-8 -*-
from troia_client.rest_troia_new_client import TroiaNewClient
import sys
import unittest

sys.path.append('../')

class TestClient(unittest.TestCase):

    base_url = "http://localhost:8080/GetAnotherLabel/"

    def setUp(self):
        self.tc = TroiaNewClient(self.base_url)
#        self.tc.put_job(self.ID)
#        self.tc.load_categories(self._labels(), self.ID)

    def tearDown(self):
        self.tc.delete_job()

    def testPing(self):
        r = self.tc.ping()
        self.assertTrue(r['status'] == 'Success')
        # I wanted to parse date but it its in some wired form so..

    def testAllMethods(self):
        for method_name in sorted([method for method in dir(self.tc) if callable(getattr(self.tc, method))], reverse=True):
            if not method_name.startswith("_"):
                print method_name
                try:
                    res = getattr(self.tc, method_name)()
                    print 'OK', res
                except Exception as ex:
                    print ex
                print '\n'

if __name__ == '__main__':
    unittest.main()
