import unittest
from bowling import PlayerLine, Frame


class BowlingTestCase(unittest.TestCase):

    def test_bowling_all_strikes(self):
        line = PlayerLine('XXXXXXXXXXXX')
        self.assertEqual(line.score, 300)

    def test_bowling_no_special(self):
        line = PlayerLine('9-9-9-9-9-9-9-9-9-9-')
        self.assertEqual(line.score, 90)

    def test_bowling_all_spares(self):
        line = PlayerLine('5/5/5/5/5/5/5/5/5/5/5')
        self.assertEqual(line.score, 150)

    def test_bowling_mixed_frames(self):
        line = PlayerLine('X7/9-X-88/-6XXX81')
        self.assertEqual(line.score, 167)

    def test_empty_line_score_0(self):
        line = PlayerLine()
        self.assertEqual(line.score, 0)


class FrameTestCase(unittest.TestCase):
    def test_frame_default_returns_empty_frame(self):
        f = Frame()
        self.assertEqual(f.next.line_score, 0)

    def test_frame_next_recursive(self):
        f = Frame()
        self.assertEqual(f.next.next.next.line_score, 0)

