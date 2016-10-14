

class PlayerLine(object):

    def __init__(self, game_results=''):
        self.frames = self.frames_from_results(list(game_results))

    @property
    def score(self):
        return sum(f.line_score for f in self.frames)

    def frames_from_results(self, game_results):
        """
        Parses a game result list into frame objects.
        """
        NEXT_THROW = 0
        frames = []
        last_roll = None

        while game_results:
            current_roll = game_results.pop(NEXT_THROW)
            if current_roll == Strike.TOKEN:
                frames.append(Strike())

            elif current_roll == Spare.TOKEN:
                frames.append(Spare(first_roll=int(last_roll)))
                last_roll = None

            elif current_roll == RegularHit.MISS_TOKEN:
                frames.append(RegularHit(
                    first_roll=int(last_roll)
                ))
                last_roll = None

            elif last_roll:
                # two hits
                frames.append(RegularHit(
                    first_roll=int(last_roll),
                    second_roll=int(current_roll)
                ))
                last_roll = None

            else:
                last_roll = current_roll

        return frames


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
    TOKEN = 'X'
    frame_points = 10

    @property
    def line_score(self):
        return 10 + self.next.frame_points + self.next.next.frame_points


class Spare(Frame):
    TOKEN = '/'

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
    MISS_TOKEN = '-'

    @property
    def line_score(self):
        return self.first_roll + self.second_roll

