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


class Strategy1:
    @staticmethod
    def _map_file_choice(choice: str) -> Choice:
        match choice:
            case "A" | "X":
                return Choice.ROCK
            case "B" | "Y":
                return Choice.PAPER
            case "C" | "Z":
                return Choice.SCISSORS

    @staticmethod
    def _load_file(file_name: str):
        with open(file_name, "rt") as file:
            return (line.split(" ") for line in file.read().splitlines())

    @classmethod
    def apply_strategy(cls, instructions, game: Game) -> Game:
        player1_moves = []
        player2_moves = []
        for i1, i2 in instructions:
            player1_moves.append(cls._map_file_choice(i1))
            player2_moves.append(cls._map_file_choice(i2))
        game.add_player(player1_moves)
        game.add_player(player2_moves)
        return game

    @classmethod
    def from_file(cls, file_name):
        game = Game()
        game = cls.apply_strategy(cls._load_file(file_name), game)
        return game


class Strategy2(Strategy1):
    @staticmethod
    def _map_strategy(opponent_choice: Choice, expected_result: str) -> Choice:
        result = None
        match expected_result, opponent_choice:
            case "Y", _:
                result = opponent_choice
            case ("X", Choice.ROCK) | ("Z", Choice.PAPER):
                result = Choice.SCISSORS
            case ("X", Choice.SCISSORS) | ("Z", Choice.ROCK):
                result = Choice.PAPER
            case ("X", Choice.PAPER) | ("Z", Choice.SCISSORS):
                result = Choice.ROCK
        return result

    @classmethod
    def apply_strategy(cls, instructions, game: Game) -> Game:
        player1_moves = []
        player2_moves = []
        for i1, i2 in instructions:
            player1_move = cls._map_file_choice(i1)
            player1_moves.append(player1_move)
            player2_moves.append(cls._map_strategy(player1_move, i2))
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


class StrategySetUpTheGame(unittest.TestCase):
    def test_loading_strategy_instructions_from_file(self):
        with patch(f"{__name__}.open", mock_open(read_data="A X\nB Y\n")) as m:
            result = tuple(Strategy1._load_file(file_name="2.in"))
        m.assert_called_once_with("2.in", "rt")
        self.assertEqual((["A", "X"], ["B", "Y"]), result)

    def test_interpret_instructions_by_strategy1(self):
        with patch.object(Strategy1, "_load_file", return_value=(["A", "X"], ["B", "Y"])):
            game = Strategy1.from_file(file_name="2.in")
        player1 = game.get_player(no=1)
        self.assertEqual([Choice.ROCK, Choice.PAPER], player1.moves)
        player2 = game.get_player(no=2)
        self.assertEqual([Choice.ROCK, Choice.PAPER], player2.moves)

    def test_interpret_instructions_by_strategy2(self):
        with patch.object(Strategy2, "_load_file", return_value=(["A", "X"], ["B", "Y"], ["C", "Z"])):
            game = Strategy2.from_file(file_name="2.in")
        player1 = game.get_player(no=1)
        self.assertEqual([Choice.ROCK, Choice.PAPER, Choice.SCISSORS], player1.moves)
        player2 = game.get_player(no=2)
        self.assertEqual([Choice.SCISSORS, Choice.PAPER, Choice.ROCK], player2.moves)


if __name__ == "__main__":
    game = Strategy1.from_file(file_name="2.in")
    game.play()
    print("Player2 score based on 1st strategy: ", game.score_for(player_no=2))
    game2 = Strategy2.from_file(file_name="2.in")
    game2.play()
    print("Player2 score based on 2st strategy: ", game2.score_for(player_no=2))
