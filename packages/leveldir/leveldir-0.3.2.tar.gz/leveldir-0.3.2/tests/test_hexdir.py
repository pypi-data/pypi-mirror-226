# standard imports
import unittest
import tempfile
import shutil
import logging
import os

# local imports
from leveldir.hex import HexDir

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()


class HexDirTest(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mkdtemp() 
        self.hexdir = HexDir(os.path.join(self.dir, 'q'), 4, 3, 2)
        logg.debug('setup hexdir root {}'.format(self.dir))
      

    def tearDown(self):
        shutil.rmtree(self.dir)
        logg.debug('cleaned hexdir root {}'.format(self.dir))


    def test_path(self):
        content = b'cdef'
        prefix = b'ab'
        label = b'\xde\xad\xbe\xef'
        (c, entry_path) = self.hexdir.add(label, content, prefix=prefix)
        
        file_path = os.path.join(self.dir, 'q', 'DE', 'AD', 'BE', label.hex().upper())
        self.assertEqual(file_path, entry_path)
        
        f = open(file_path, 'rb')
        r = f.read()
        f.close()
        self.assertEqual(content, r)

        f = open(self.hexdir.master_file, 'rb')
        r = f.read()
        f.close()
        self.assertEqual(prefix + label, r)


    def test_size(self):
        content = b'cdef'
        prefix = b'ab'
        label = b'\xde\xad\xbe\xef'
        with self.assertRaises(ValueError):
            self.hexdir.add(label, content, prefix=b'a')


    def test_index(self):
        self.hexdir.add(b'\xde\xad\xbe\xef', b'foo', b'ab')
        self.hexdir.add(b'\xbe\xef\xfe\xed', b'bar', b'cd')
        (c, entry_path) = self.hexdir.add(b'\x01\x02\x03\x04', b'baz', b'ef')
        self.assertEqual(c, 2)


    def test_edit(self):
        self.hexdir.add(b'\xde\xad\xbe\xef', b'foo', b'ab')
        self.hexdir.add(b'\xbe\xef\xfe\xed', b'bar', b'cd')
        self.hexdir.add(b'\x01\x02\x03\x04', b'baz', b'ef')
        self.hexdir.set_prefix(1, b'ff')

        f = open(self.hexdir.master_file, 'rb')
        f.seek(6)
        r = f.read(2)
        f.close()
        self.assertEqual(b'ff', r)


    def test_get(self):
        self.hexdir.add(b'\xde\xad\xbe\xef', b'foo', b'ab')
        self.hexdir.add(b'\xbe\xef\xfe\xed', b'bar', b'cd')
        self.hexdir.add(b'\x01\x02\x03\x04', b'baz', b'ef')
        (prefix, key) = self.hexdir.get(1)
        self.assertEqual(b'\xbe\xef\xfe\xed', key)
        self.assertEqual(b'cd', prefix)


class HexDirTestFormatter(unittest.TestCase):

    def setUp(self):
        def lower_formatter(hx):
            return hx.lower()
        self.dir = tempfile.mkdtemp() 
        self.hexdir = HexDir(os.path.join(self.dir, 'q'), 4, 3, 2, formatter=lower_formatter)
        logg.debug('setup hexdir root {}'.format(self.dir))


    def test_format(self):
        self.hexdir.add(b'\xaa\xbb\xcc\xdd', b'foo', b'ab')
        (prefix, key) = self.hexdir.get(1)
        checkdir_path = os.path.join(self.hexdir.path, 'aa', 'bb', 'cc', 'aabbccdd')
        os.stat(checkdir_path)
        

if __name__ == '__main__':
    unittest.main()
