import logging
import sys


logging.basicConfig(stream=sys.stdout,level=logging.DEBUG)


class Frames(list):

    def append(self, frame):
        """
        Adds a reference from `frame` to the last bowled frame, if any.
        then adds the `frame` to the list.  Can't add the frame to the list
        first or it will reference itself.
        """
        self.add_frame_reference(frame)
        super(Frames, self).append(frame)

    def add_frame_reference(self, current_frame):
        """
        Adds a reference from last frame to the current frame,
        if there is at least one bowled frame.
        """
        LAST_FRAME = -1
        if self:
            self[LAST_FRAME].next = current_frame


class LineStringFramesParser(object):
    def __init__(self, game_results=''):
        self.game_results = game_results

    @property
    def frames(self):
        return self.frames_from_results(list(self.game_results))

    def frames_from_results(self, game_results):
        """
        Parses a game result list into frame objects.
        """
        NEXT_THROW = 0
        frames = Frames()
        last_roll = None

        while game_results:
            current_roll = game_results.pop(NEXT_THROW)
            if current_roll == Strike.TOKEN:
                current_frame = Strike()
                frames.append(current_frame)

            elif current_roll == Spare.TOKEN:
                current_frame = Spare(first_roll=int(last_roll))
                last_roll = None
                frames.append(current_frame)

            elif self.is_first_miss(current_roll, last_roll):
                last_roll = 0

            elif self.is_second_miss(current_roll, last_roll):
                current_frame = OpenFrame(first_roll=int(last_roll))
                last_roll = None
                frames.append(current_frame)

            elif last_roll is not None:
                # two hits
                current_frame = OpenFrame(
                    first_roll=int(last_roll),
                    second_roll=int(current_roll)
                )
                frames.append(current_frame)
                last_roll = None

            elif not game_results:
                # if there are no more results, have to create from the
                # last action
                current_frame = OpenFrame(first_roll=int(current_roll))
                frames.append(current_frame)

            else:
                last_roll = current_roll

        return frames

    def is_first_miss(self, current_roll, last_roll):
        return (
            current_roll == OpenFrame.MISS_TOKEN
            and last_roll is None
        )

    def is_second_miss(self, current_roll, last_roll):
        return (
            current_roll == OpenFrame.MISS_TOKEN
            and last_roll is not None
        )


class PlayerLine(object):
    LAST_GAME_FRAME = 10

    def __init__(self, game_results=''):
        self.frames = LineStringFramesParser(game_results).frames

    @property
    def score(self):
        """
        Calculates the players current score from the line.

        Scores after the last frame are only used to calculate the last
        frame's score
        """
        return sum(f.line_score(is_last_frame=i >= self.LAST_GAME_FRAME)
                   for i, f in enumerate(self.frames))


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
    points = 0
    _next = None

    def __init__(self, first_roll=0, second_roll=None):
        self.first_roll = first_roll
        self.second_roll = second_roll

    @property
    def next(self):
        return self._next if self._next else Frame()

    @next.setter
    def next(self, frame):
        self._next = frame

    def line_score(self, is_last_frame=False):
        return 0


class Strike(Frame):
    TOKEN = 'X'

    def __init__(self, first_roll=10, second_roll=None):
        self.first_roll = first_roll
        self.second_roll = second_roll

    def line_score(self, is_last_frame=False):
        """
        Calculates ten plus the simple total of the pins knocked down
        in his next two rolls.
        """
        if is_last_frame:
            return 0

        # next two rolls could span 2 frames
        next_first_roll = self.next.first_roll
        if self.next.second_roll is not None:
            next_second_roll = self.next.second_roll
        else:
            next_second_roll = self.next.next.first_roll

        logging.debug('(10 + {} + {})'.format(
            next_first_roll, next_second_roll
        ))
        return 10 + next_first_roll + next_second_roll


class Spare(Frame):
    TOKEN = '/'

    def __init__(self, first_roll=0, second_roll=0):
        self.first_roll = first_roll
        self.second_roll = 10 - self.first_roll

    def line_score(self, is_last_frame=False):
        if is_last_frame:
            return 0

        logging.debug('({} + {} + {})'.format(
            self.first_roll,
            self.second_roll,
            self.next.first_roll
        ))
        return 10 + self.next.first_roll


class OpenFrame(Frame):
    MISS_TOKEN = '-'

    def line_score(self, is_last_frame=False):
        if is_last_frame:
            return 0

        logging.debug('({} + {})'.format(self.first_roll, self.second_roll))
        return self.first_roll + (self.second_roll or 0)

