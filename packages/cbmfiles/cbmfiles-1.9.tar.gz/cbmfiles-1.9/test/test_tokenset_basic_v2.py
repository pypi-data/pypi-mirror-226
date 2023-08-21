import unittest

from cbm_files.tokenset_basic_v2 import TokenSet_BASICv2


class TestBasicV2(unittest.TestCase):
    def test_tokenize(self):
        tokenset = TokenSet_BASICv2()
        self.assertEqual(tokenset.tokenize('SYS', 'ascii'), b'\x9e')
        self.assertEqual(tokenset.tokenize('sys', 'ascii'), b'\x9e')
        self.assertEqual(tokenset.tokenize('GOTO', 'ascii'), b'\x89')
        self.assertEqual(tokenset.tokenize('GO TO', 'ascii'), b'\xcb \xa4')
        self.assertEqual(tokenset.tokenize('INPUTA', 'ascii'), b'\x85A')
        self.assertEqual(tokenset.tokenize('INPUT#2', 'ascii'), b'\x842')
        self.assertEqual(tokenset.tokenize('GOSU:', 'ascii'), b'\xcbSU:')
        self.assertEqual(tokenset.tokenize('WAND128', 'ascii'), b'W\xaf128')
        self.assertEqual(tokenset.tokenize('A=RND(1)', 'ascii'), b'A\xb2\xbb(1)')
        self.assertEqual(tokenset.tokenize('3↑2', 'ascii'), b'3\xae2')
        self.assertEqual(tokenset.tokenize('3^2', 'ascii'), b'3\xae2')
        self.assertEqual(tokenset.tokenize('REM SHORT', 'ascii'), b'\x8f SHORT')
        self.assertEqual(tokenset.tokenize('DATA STOP:STOP', 'ascii'), b'\x83 STOP:\x90')
        self.assertEqual(tokenset.tokenize('REM STOP:STOP', 'ascii'), b'\x8f STOP:STOP')

    def test_expand(self):
        tokenset = TokenSet_BASICv2()
        self.assertEqual(tokenset.expand(b'\x9e', 'ascii'), 'SYS')
        self.assertEqual(tokenset.expand(b'A\xb2\xbb(1)', 'ascii'), 'A=RND(1)')
        self.assertEqual(tokenset.expand(b'3\xae2', 'ascii'), '3^2')

    def test_renumber_split(self):
        tokenset = TokenSet_BASICv2()
        # 'GOTO10:PRINT20'
        self.assertEqual(list(tokenset.renumber_split(b'\x8910:\x9920')), [b'\x89', 10, b':\x9920'])
        # 'ONAGOTO10,20'
        self.assertEqual(list(tokenset.renumber_split(b'\x91A\x8910,20')), [b'\x91A\x89', 10, b',', 20])
        # 'PRINT"<$8D>5"'
        self.assertEqual(list(tokenset.renumber_split(b'\x99"\x8D5"')), [b'\x99"\x8D5"'])
        # 'GO TO 30'
        self.assertEqual(list(tokenset.renumber_split(b'\xCB \xA4 30')), [b'\xCB \xA4 ', 30])
        # 'LIST40-50'
        self.assertEqual(list(tokenset.renumber_split(b'\x9B40\xAB50')), [b'\x9B', 40, b'\xAB', 50])
