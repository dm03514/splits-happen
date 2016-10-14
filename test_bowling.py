import unittest
from bowling import PlayerLine, Frame, Strike, Spare, OpenFrame


class BowlingTestCase(unittest.TestCase):

    def test_bowling_all_strikes(self):
        line = PlayerLine('XXXXXXXXXXXX')
        self.assertEqual(line.score, 300)

    def test_bowling_no_special(self):
        line = PlayerLine('9-9-9-9-9-9-9-9-9-9-')
        self.assertEqual(line.score, 90)

    def test_bowling_all_spares(self):
        line = PlayerLine('5/5/5/5/5/5/5/5/5/5/5')
        self.assertEqual(len(line.frames), 11)
        self.assertEqual(line.score, 150)

    def test_bowling_mixed_frames(self):
        line = PlayerLine('X7/9-X-88/-6XXX81')
        self.assertEqual(len(line.frames), 11)
        self.assertEqual(line.score, 167)

    def test_empty_line_score_0(self):
        line = PlayerLine()
        self.assertEqual(line.score, 0)

    def test_player_line_parse_strike(self):
        line = PlayerLine('X')
        self.assertEqual(len(line.frames), 1)
        self.assertIsInstance(line.frames[0], Strike)

    def test_player_line_parse_spare(self):
        line = PlayerLine('9/')
        self.assertEqual(len(line.frames), 1)
        self.assertIsInstance(line.frames[0], Spare)
        self.assertEqual(line.frames[0].first_roll, 9)

    def test_player_line_parse_two_hits(self):
        line = PlayerLine('73')
        self.assertEqual(len(line.frames), 1)
        self.assertIsInstance(line.frames[0], OpenFrame)
        self.assertEqual(line.frames[0].first_roll, 7)
        self.assertEqual(line.frames[0].second_roll, 3)

    def test_player_line_parse_single_hit(self):
        line = PlayerLine('7-')
        self.assertEqual(len(line.frames), 1)
        self.assertIsInstance(line.frames[0], OpenFrame)
        self.assertEqual(line.frames[0].first_roll, 7)
        self.assertEqual(line.frames[0].second_roll, None)


class FrameTestCase(unittest.TestCase):
    def test_frame_default_returns_empty_frame(self):
        f = Frame()
        self.assertEqual(f.next.line_score(), 0)

    def test_frame_next_recursive(self):
        f = Frame()
        self.assertEqual(f.next.next.next.line_score(), 0)

