import unittest
from enum import IntEnum


class Choice(IntEnum):
    ROCK = 1
    SCISSORS = 3


class MatchResult(IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6


class Game:
    @staticmethod
    def play_match(player1: Choice, player2: Choice) -> MatchResult:
        """Returns match result from the perspective of player1"""
        result = None
        match player1, player2:
            case Choice.ROCK, Choice.SCISSORS:
                result = MatchResult.WIN
        return result


class MatchResultTestCase(unittest.TestCase):
    def test_rock_defeats_scissors(self):
        match_result = Game.play_match(Choice.ROCK, Choice.SCISSORS)
        self.assertEqual(MatchResult.WIN, match_result)
