import math
from module_0.guess_number import game_core_v3
from unittest import TestCase


class GuessNumberTest(TestCase):
    def test_game_core_v3(self):
        for ll in range(1, 100):
            for ul in range(100, 201):
                # for max count add 2 due to specific of log function and ceil() and floor() used in game_core_v3
                max_count = math.ceil(math.log2(ul - ll)) + 2
                for n in range(ll, ul + 1):
                    number, count = game_core_v3(n, ll, ul)
                    self.assertEqual(number, n,
                         f'll={ll}, ul={ul}, n={n}, max_count={max_count}, number={number}, count={count}')
                    self.assertLessEqual(count, max_count,
                         f'll={ll}, ul={ul}, n={n}, number={number}, max_count={max_count}, count={count}')
