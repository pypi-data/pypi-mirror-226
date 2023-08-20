# standard imports
import unittest
import argparse

# local imports
from aiee.arg import (
        ArgFlag,
        Arg,
        process_args,
        )


class TestArg(unittest.TestCase):

    def test_arg(self):
        flag = ArgFlag()
        flag.add('foo')
        flag.add('bar')
        flag.alias('baz', flag.FOO, flag.BAR)

        arg = Arg(flag)
        arg.add('x', 'baz')
        r = arg.get('baz')[0]

        self.assertEqual(r[0], '-x')
        self.assertIsNone(r[1])
        self.assertEqual(r[2], 'x')

        arg.set_long('x', 'xyzzy')
        r = arg.get('baz')[0]
        self.assertEqual(r[0], '-x')
        self.assertEqual(r[1], '--xyzzy')
        self.assertEqual(r[2], 'x')

        arg.add('y', 'foo', dest='yyy')
        r = arg.get('foo')[0]
        self.assertEqual(r[0], '-y')
        self.assertIsNone(r[1])
        self.assertEqual(r[2], 'yyy')

        arg.set_long('y', 'yy', dest='yyyyy')
        r = arg.get('foo')[0]
        self.assertEqual(r[0], '-y')
        self.assertEqual(r[1], '--yy')
        self.assertEqual(r[2], 'yyyyy')


    def test_arg_multi(self):
        flag = ArgFlag()
        flag.add('foo')

        arg = Arg(flag)
        arg.add('x', 'foo')
        arg.add('y', 'foo')

        r = arg.get('foo')
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0][0], '-x')
        self.assertEqual(r[1][0], '-y')


    def test_arg_longonly(self):
        flag = ArgFlag()
        flag.add('foo')

        arg = Arg(flag)
        arg.add('x', 'foo')
        arg.add_long('yyy', 'foo')

        r = arg.get('foo')
        self.assertEqual(len(r), 2)
        self.assertEqual(r[0][0], '-x')
        self.assertEqual(r[1][1], '--yyy')


    def test_arg_iter(self):
        flags = ArgFlag()
        flags.add('foo')
        flags.add('bar')

        r = []
        arg = Arg(flags)
        for flag in arg:
            r.append(flag)

        self.assertEqual(len(r), 0)

        r = []
        arg.add('y', 'bar')
        for flag in arg:
            r.append(flag)
        self.assertListEqual(r, [flags.BAR])

        r = []
        arg.add('x', 'foo')
        for flag in arg:
            r.append(flag)
        self.assertListEqual(r, [flags.FOO, flags.BAR])


    def test_arg_iter_mix(self):
        flags = ArgFlag()
        flags.add('foo')
        flags.add('bar')

        arg = Arg(flags)

        r = []
        arg.add('y', 'bar')
        for flag in arg:
            r.append(flag)
        self.assertListEqual(r, [flags.BAR])

        r = []
        arg.add_long('xxx', 'foo')
        for flag in arg:
            r.append(flag)
        self.assertListEqual(r, [flags.FOO, flags.BAR])


    def test_process_argparser(self):
        flags = ArgFlag()
        flags.add('foo')

        arg = Arg(flags)
        arg.add('x', 'foo')

        argparser = argparse.ArgumentParser()
        argparser = process_args(argparser, arg, flags.FOO)
        r = argparser.parse_args(['-x', '13'])

        self.assertEqual(r.x, '13')

    
    def test_process_argparser_multi(self):
        flags = ArgFlag()
        flags.add('foo')

        arg = Arg(flags)
        arg.add('x', 'foo')
        arg.add('y', 'foo')
        arg.add_long('zzz', 'foo')

        argparser = argparse.ArgumentParser()
        argparser = process_args(argparser, arg, flags.FOO)
        r = argparser.parse_args(['-x', '13', '-y', '42', '--zzz', '666'])

        self.assertEqual(r.x, '13')
        self.assertEqual(r.y, '42')
        self.assertEqual(r.zzz, '666')


    def test_process_argparser_multi_alias(self):
        flags = ArgFlag()
        flags.add('foo')
        flags.add('bar')
        flags.alias('baz', 'foo', 'bar')

        arg = Arg(flags)
        arg.add('x', 'foo')
        arg.add('y', 'bar')

        argparser = argparse.ArgumentParser()
        argparser = process_args(argparser, arg, flags.BAZ)
        r = argparser.parse_args(['-x', '13', '-y', '42'])

        self.assertEqual(r.x, '13')
        self.assertEqual(r.y, '42')


    def test_process_argparser_multi_alias_selective(self):
        flags = ArgFlag()
        flags.add('foo')
        flags.add('bar')
        flags.alias('baz', 'foo', 'bar')

        arg = Arg(flags)
        arg.add('y', 'bar')

        argparser = argparse.ArgumentParser()
        argparser = process_args(argparser, arg, flags.BAZ)
        r = argparser.parse_args(['-y', '42'])

        self.assertEqual(r.y, '42')

        argparser = argparse.ArgumentParser()
        argparser = process_args(argparser, arg, flags.FOO)

        with self.assertRaises(SystemExit):
            r = argparser.parse_args(['-y', '42'])


    def test_process_argparser_typ(self):
        flags = ArgFlag()
        flags.add('foo')

        arg = Arg(flags)
        arg.add('x', 'foo', typ=int)

        argparser = argparse.ArgumentParser()
        argparser = process_args(argparser, arg, flags.FOO)
        
        r = argparser.parse_args(['-x', '13'])

        self.assertEqual(r.x, 13)


    def test_xargs(self):
        flags = ArgFlag()
        flags.add('foo')
        
        args = Arg(flags)
        args.add('x', 'foo', action='append', help='bah')

        argparser = argparse.ArgumentParser()
        argparser = process_args(argparser, args, flags.FOO)

        r = argparser.parse_args(['-x', '13', '-x', '42'])
        self.assertListEqual(r.x, ['13', '42'])

        args.add('y', 'foo', help='snuh', me='bar')
        argparser = argparse.ArgumentParser()

        with self.assertRaises(TypeError):
            process_args(argparser, args, flags)


    def test_bool_type(self):
        flags = ArgFlag()
        flags.add('foo')
        
        args = Arg(flags)
        args.add('x', 'foo', typ=bool)

        argparser = argparse.ArgumentParser()
        argparser = process_args(argparser, args, flags.FOO)

        r = argparser.parse_args(['-x'])

        self.assertIsInstance(r.x, bool)


    def test_val(self):
        flags = ArgFlag()
        flags.add('foo')
        
        args = Arg(flags)
        args.add('x', 'foo', typ=bool)

        r = args.val('foo')
        self.assertEqual(r, flags.FOO)


    def test_match(self):
        flags = ArgFlag()
        flags.add('foo')
        flags.add('bar')
        flags.alias('baz', 'foo', 'bar')
        
        args = Arg(flags)
        args.add('x', 'foo', typ=bool)
        self.assertFalse(args.match('foo', 0))
        self.assertTrue(args.match('foo', flags.FOO))
        self.assertFalse(args.match('bar', flags.BAR))
        self.assertFalse(args.match('bar', flags.BAZ))
        self.assertFalse(args.match('baz', flags.BAR))
        self.assertFalse(args.match('baz', flags.BAZ))

        args.add('y', 'bar', typ=bool)
        self.assertTrue(args.match('foo', flags.FOO))
        self.assertTrue(args.match('bar', flags.BAR))
        self.assertTrue(args.match('bar', flags.BAZ))
        self.assertFalse(args.match('baz', flags.BAR))
        self.assertTrue(args.match('baz', flags.BAZ))


if __name__ == '__main__':
    unittest.main()
