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
    def __init__(self):
        self._players = []

    @property
    def has_enough_players(self):
        return len(self._players) == 2

    @staticmethod
    def play_match(player1: Choice, player2: Choice) -> MatchResult:
        """Returns match result from the perspective of player1"""
        result = None
        match player1, player2:
            case (Choice.ROCK, Choice.SCISSORS) | (Choice.SCISSORS, Choice.PAPER) | (Choice.PAPER, Choice.ROCK):
                result = MatchResult.WIN
            case (Choice.SCISSORS, Choice.ROCK) | (Choice.PAPER, Choice.SCISSORS) | (Choice.ROCK, Choice.PAPER):
                result = MatchResult.LOSS
            case _ if player1 == player2:
                result = MatchResult.DRAW
        return result

    def play(self):
        if not self.has_enough_players:
            raise RuntimeError("Not enough players to play the game! We need 2. Please add player to the game.")

    def add_player(self, moves: list[Choice]) -> int:
        self._players.append(moves)
        return len(self._players)


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

    def test_losses(self):
        for player2, player1 in self.combinations:
            match_result = Game.play_match(player1, player2)
            self.assertEqual(MatchResult.LOSS, match_result, f"{player1.name} vs {player2.name}")

    def test_draws(self):
        for choice in (Choice.ROCK, Choice.PAPER, Choice.SCISSORS):
            match_result = Game.play_match(choice, choice)
            self.assertEqual(MatchResult.DRAW, match_result, f"{choice.name} vs {choice.name}")


class GameResultTestCase(unittest.TestCase):
    def test_play_game_without_players(self):
        game = Game()
        with self.assertRaises(RuntimeError):
            game.play()

    def test_play_game_with_one_player(self):
        game = Game()
        player_no = game.add_player([])
        self.assertEqual(1, player_no)
        with self.assertRaises(RuntimeError):
            game.play()
