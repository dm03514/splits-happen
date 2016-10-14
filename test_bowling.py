import unittest
from bowling import PlayerGame


class BowlingTestCase(unittest.TestCase):

    def test_bowling_all_strikes(self):
        game = PlayerGame('XXXXXXXXXXXX')
        self.assertEqual(game.score, 300)

    def test_bowling_no_special(self):
        game = PlayerGame('9-9-9-9-9-9-9-9-9-9-')
        self.assertEqual(game.score, 90)

    def test_bowling_all_spares(self):
        game = PlayerGame('5/5/5/5/5/5/5/5/5/5/5')
        self.assertEqual(game.score, 150)

    def test_bowling_mixed_frames(self):
        game = PlayerGame('X7/9-X-88/-6XXX81')
        self.assertEqual(game.score, 167)

