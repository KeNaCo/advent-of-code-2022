import unittest
from enum import IntEnum


class Choice(IntEnum):
    ROCK = 1
    PAPER = 2
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
            case (Choice.ROCK, Choice.SCISSORS) | (Choice.SCISSORS, Choice.PAPER) | (Choice.PAPER, Choice.ROCK):
                result = MatchResult.WIN
        return result


class MatchResultTestCase(unittest.TestCase):
    combinations = (
        (Choice.ROCK, Choice.SCISSORS),
        (Choice.SCISSORS, Choice.PAPER),
        (Choice.PAPER, Choice.ROCK),
    )

    def test_wins(self):
        for player1, player2 in self.combinations:
            match_result = Game.play_match(player1, player2)
            self.assertEqual(MatchResult.WIN, match_result, f"{player1.name} vs {player2.name}")
