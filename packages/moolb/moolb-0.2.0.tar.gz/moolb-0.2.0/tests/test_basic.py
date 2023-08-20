import unittest
import hashlib
import logging

from moolb import Bloom

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


def hashround(self, b, s):
       logg.debug('sha1 hashing {} {}'.format(b.hex(), s.hex()))
       h = hashlib.sha1()
       h.update(b)
       h.update(s)
       return h.digest()


class Test(unittest.TestCase):

    def test_basic(self):
        f = Bloom(8192 * 8, 3)
        f.add(b'1024')
        self.assertTrue(f.check(b'1024'))
        self.assertFalse(f.check(b'1023'))


    def test_defaul(self):
        b = bytearray(8192)
        b[42] = 13
        f = Bloom(8192 * 8, 3, default_data=b)
        self.assertEqual(f.filter[42], 13)
        
        b = bytearray(8193)
        with self.assertRaises(ValueError):
            f = Bloom(8192 * 8, 3, default_data=b)
   

    def test_plug(self):
        f = Bloom(8192 * 8, 3, hashround)
        f.add(b'1024')
        self.assertTrue(f.check(b'1024'))
        self.assertFalse(f.check(b'1023'))


    def test_merge(self):
        f = Bloom(8 * 8, 3, hashround)
        b = bytearray(8)
        b[2] = 2
        b[6] = 4
        f.merge(b)
        self.assertEqual(f.filter[2], 2)
        self.assertEqual(f.filter[6], 4)

        b = bytearray(8)
        b[2] = 1
        b[6] = 8
        f.merge(b)
        self.assertEqual(f.filter[2], 3)
        self.assertEqual(f.filter[6], 12)

        b = bytearray(9)
        with self.assertRaises(ValueError):
            f.merge(b)


#    def test_dump(self):
#        f = Bloom(8192 * 8, 3)
#        f.add(b'1024')
#        logg.debug(f.to_bytes().hex())

if __name__ == '__main__':
    unittest.main()
