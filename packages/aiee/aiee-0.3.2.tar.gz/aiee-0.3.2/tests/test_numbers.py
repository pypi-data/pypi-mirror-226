# standard imports
import unittest

# local imports
from aiee.numbers import postfix_to_int


class TestNumbers(unittest.TestCase):

    def test_postfix(self):

        for v in [
                [42, 42, 0],
                [1.0, 10, 1],
                [3.14, 314, 2],
                [0.667, 667, 3],
                ]:

            s = str(v[0])

            for i, p in enumerate([
                '',
                'k',
                'm',
                'g',
                't',
                'p',
                'e',
                'z',
                'y',
                ]):
                r = postfix_to_int(s + p)
                x = v[1] * (10 ** ((i * 3) - v[2]))
                self.assertEqual(int(x), r)

        r = postfix_to_int('42E11')
        x = 42 * (10 ** 11)
        self.assertEqual(x, r)


if __name__ == '__main__':
    unittest.main()
