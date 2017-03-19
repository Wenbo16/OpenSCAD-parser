import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_assert(self):
        chart =  [ [('P', 'S', 0, 0, ()), ('S', 'S + M', 0, 0, ())],
                   [('T', '2', 1, 0, ()), ('M', 'T', 1, 0, ((1, 0),))]]

        self.assertEqual( chart,
                          [[('P', 'S', 0, 0, ()), ('S', 'S + M', 0, 0, ())],
                           [('T', '2', 1, 0, ()), ('M', 'T', 1, 0, ((1, 0),))]])

if __name__ == '__main__':
    unittest.main()