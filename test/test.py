
import sys
import unittest

sys.path.append('..')

import plsgrab

class TestScanFunctions(unittest.TestCase):

    def setUp(self):
        with open("test.pls", 'r') as file:
            self.plstext = file.read()
        with open("test.html", 'r') as file:
            self.htmltext = file.read()


    def test_extract_pls(self):
        self.assertEqual(plsgrab.extract_pls(self.plstext), 'http://uwstream2.somafm.com:80')


    def test_extract_urls(self):
        self.assertEqual(plsgrab.get_multiple_pls(self.htmltext),
                         ['http://somafm.com/dronezone.pls',
                          'http://somafm.com/dronezone24.pls',
                          'http://somafm.com/dronezone56.pls',
                          'http://somafm.com/dronezone130.pls',
                          'http://somafm.com/dronezone32.pls',
                          'http://somafm.com/dronezone64.pls'])


if __name__ == '__main__':
    unittest.main()
