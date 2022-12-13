import unittest
from collections import deque
from dataclasses import dataclass


@dataclass(slots=True)
class StacksArea:
    _stacks: tuple[deque[str]]

    @classmethod
    def from_string(cls, input: str) -> "StacksArea":
        if not input:
            return StacksArea(tuple())

    def __len__(self):
        return len(self._stacks)


class CreateStacksArea(unittest.TestCase):
    def test_empty_input_should_return_empty_stacks_area(self):
        stacks_area = StacksArea.from_string("")
        self.assertEqual(0, len(stacks_area))
