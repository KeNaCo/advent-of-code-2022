import unittest
from dataclasses import dataclass
from enum import IntEnum
from unittest.mock import patch, mock_open


class Choice(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class MatchResult(IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6

    def opposite(self):
        if self == MatchResult.LOSS:
            return MatchResult.WIN
        elif self == MatchResult.WIN:
            return MatchResult.LOSS
        else:
            return MatchResult.DRAW


@dataclass
class Player:
    moves: list[Choice]
    results: list[MatchResult]


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

    def play(self) -> int:
        """
        :return: Number of matches played during one game.
        """
        if not self.has_enough_players:
            raise RuntimeError("Not enough players to play the game! We need 2. Please add player to the game.")

        player1 = self.get_player(1)
        player2 = self.get_player(2)
        for player1_choice, player2_choice in zip(player1.moves, player2.moves, strict=True):
            result = self.play_match(player1_choice, player2_choice)
            player1.results.append(result)
            player2.results.append(result.opposite())

        return len(self._players[0].results)

    def add_player(self, moves: list[Choice]) -> int:
        self._players.append(Player(moves, []))
        return len(self._players)

    def get_player(self, no: int) -> Player:
        return self._players[no - 1]

    def score_for(self, player_no: int) -> int:
        player = self.get_player(player_no)
        return sum(player.moves) + sum(player.results)

    @staticmethod
    def map_file_choice(choice: str) -> Choice:
        match choice:
            case "A" | "X":
                return Choice.ROCK
            case "B" | "Y":
                return Choice.PAPER
            case "C" | "Z":
                return Choice.SCISSORS

    @classmethod
    def from_file(cls, file_name):
        player1_moves = []
        player2_moves = []
        with open(file_name, "rt") as file:
            for line in file.read().splitlines():
                player1, player2 = line.split(" ")
                player1_moves.append(cls.map_file_choice(player1))
                player2_moves.append(cls.map_file_choice(player2))
        game = Game()
        game.add_player(player1_moves)
        game.add_player(player2_moves)
        return game


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

    def test_play_game_with_players_without_moves(self):
        game = Game()
        player1 = game.add_player(moves=[])
        player2 = game.add_player(moves=[])
        self.assertEqual(1, player1)
        self.assertEqual(2, player2)

        matches_played = game.play()
        self.assertEqual(0, matches_played)

    def test_play_game_with_only_one_match(self):
        game = Game()
        game.add_player(moves=[Choice.ROCK])
        game.add_player(moves=[Choice.SCISSORS])
        matches_played = game.play()
        self.assertEqual(1, matches_played)

    def test_play_game_with_only_many_matches(self):
        game = Game()
        game.add_player(moves=[Choice.ROCK, Choice.ROCK])
        game.add_player(moves=[Choice.SCISSORS, Choice.ROCK])
        matches_played = game.play()
        self.assertEqual(2, matches_played)

    def test_get_score_after_game(self):
        game = Game()
        game.add_player(moves=[Choice.ROCK])
        game.add_player(moves=[Choice.SCISSORS])
        game.play()
        player1_score = game.score_for(player_no=1)
        self.assertEqual(7, player1_score)
        player2_score = game.score_for(player_no=2)
        self.assertEqual(3, player2_score)


class LoadGameFromFile(unittest.TestCase):
    def test_loading_game_from_file(self):
        with patch(f"{__name__}.open", mock_open(read_data="A X\nB Y\n")) as m:
            game = Game.from_file(file_name="2.in")
        m.assert_called_once_with("2.in", "rt")
        player1 = game.get_player(no=1)
        self.assertEqual([Choice.ROCK, Choice.PAPER], player1.moves)
        player2 = game.get_player(no=2)
        self.assertEqual([Choice.ROCK, Choice.PAPER], player2.moves)


if __name__ == "__main__":
    game = Game.from_file(file_name="2.in")
    game.play()
    print(game.score_for(player_no=2))
