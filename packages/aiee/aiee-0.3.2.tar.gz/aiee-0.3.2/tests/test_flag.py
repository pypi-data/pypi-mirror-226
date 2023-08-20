# standard imports
import unittest

# local imports
from aiee.arg import ArgFlag


class TestAieeFlag(unittest.TestCase):

    def test_basic_flag(self):
        arg = ArgFlag()
        arg.add('foo')
        arg.add('bar')

        self.assertEqual(arg.FOO, 1)
        self.assertEqual(arg.BAR, 2)

        self.assertEqual(arg.get('foo'), arg.FOO)
        self.assertEqual(arg.get('bar'), arg.BAR)

        arg.alias('baz', arg.FOO, arg.BAR)
        self.assertEqual(arg.BAZ, 3)

        arg.alias('barbarbar', 'foo', arg.BAR)
        self.assertEqual(arg.BARBARBAR, 3)

        self.assertTrue(arg.match('foo', arg.FOO))
        self.assertFalse(arg.match('foo', arg.BAR))
        self.assertTrue(arg.match('foo', arg.BAZ))

        with self.assertRaises(ValueError):
            arg.add('foo')

        with self.assertRaises(ValueError):
            arg.alias('xyzzy', 5)

        self.assertEqual(arg.val('foo'), arg.FOO)
        self.assertEqual(arg.val(arg.FOO), arg.FOO)
        self.assertEqual(arg.val(arg.BAZ), arg.BAZ)
        with self.assertRaises(ValueError):
            arg.val(4)


    def test_name_set(self):
        arg = ArgFlag()
        arg.add('foo')
        arg.add('bar')
        arg.alias('baz', arg.FOO, arg.BAR)

        self.assertEqual(arg.less('baz', arg.FOO), arg.BAR)
        self.assertEqual(arg.more('foo', arg.BAR), arg.BAZ)


    def test_name_flag(self):
        arg = ArgFlag()
        arg.add('foo')
        arg.add('bar')
        arg.alias('baz', arg.FOO, arg.BAR)

        self.assertListEqual(arg.names(arg.BAZ), ['FOO', 'BAR'])


if __name__ == '__main__':
    unittest.main()
