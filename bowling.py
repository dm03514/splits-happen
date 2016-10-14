

class PlayerLine(object):

    def __init__(self, game_results=None):
        self.game_results = game_results
        self.frames = []

    @property
    def score(self):
        return sum(f.line_score for f in self.frames)


class Frame(object):
    """
    Stores result for a player action.
    Actions are:
        - strike
        - spare
        - 2 throws

    All frames reference the next frame.  Next frames that are
    not yet played have a score of 0.

    The bonus hits in the last frame are modeled as frames,
    which should simplify the calculation.  If we expose this
    to a user we can create an abstraction around it to make
    it display as a single frame.

    There are two members:
        - line_score - the score that this frame will add
            to the line's total score
        - points - the number of points this will contribute
            to a previous frame's score
    """
    line_score = 0
    points = 0

    def __init__(self, first_roll=None, second_roll=None):
        self.first_roll = first_roll
        self.second_roll = second_roll

    @property
    def next(self):
        return Frame()


class Strike(Frame):
    frame_points = 10

    @property
    def line_score(self):
        return 10 + self.next.frame_points + self.next.next.frame_points


class Spare(Frame):

    @property
    def line_score(self):
        return 10 + self.next.frame_points

    @property
    def frame_points(self):
        """
        Spares points will always count for the first roll,
        since the second roll will qualify the frame as a spare.

        :return:
        """
        return self.first_roll


class RegularHit(Frame):

    @property
    def line_score(self):
        return self.first_roll + self.second_roll

