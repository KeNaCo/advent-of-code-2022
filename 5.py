import unittest
from collections import deque
from dataclasses import dataclass
from itertools import islice


@dataclass(slots=True)
class StacksArea:
    _stacks: tuple[deque[str]]

    @staticmethod
    def _iter_stacks(iterable):
        it = iter(iterable)
        while batch := list(islice(it, 3)):
            yield batch

    @classmethod
    def from_string(cls, input: str) -> "StacksArea":
        if not input:
            return StacksArea(tuple())

        stacks = []
        for line in input.splitlines():
            for i, crate in enumerate(cls._iter_stacks(line)):
                if crate[1] == " ":  # no stack, but we know some may be here
                    if len(stacks) <= i:  # we will initialise stack with a deque
                        stacks.append(deque())
        return cls(tuple(stacks))

    def __len__(self):
        return len(self._stacks)

    def __getitem__(self, item):
        return self._stacks[item]


class CreateStacksArea(unittest.TestCase):
    def test_empty_input_should_return_empty_stacks_area(self):
        stacks_area = StacksArea.from_string("")
        self.assertEqual(0, len(stacks_area))

    def test_empty_stack_should_be_marked_with_number(self):
        stacks_area = StacksArea.from_string("   \n 1 ")
        self.assertEqual(1, len(stacks_area))
        self.assertEqual(0, len(stacks_area[0]))
