import unittest
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from itertools import islice


@dataclass(slots=True)
class StacksArea:
    _stacks: tuple[deque[str]]

    @staticmethod
    def _iter_stacks(iterable):
        it = iter(iterable)
        # we have 3 characters representing stack space plus 1 empty space between stacks
        while batch := list(islice(it, 4)):
            yield batch[:3]

    @classmethod
    def from_string(cls, input: str) -> "StacksArea":
        if not input:
            return StacksArea(tuple())

        stacks = []
        for line in input.splitlines():
            for i, crate in enumerate(cls._iter_stacks(line)):
                match tuple(crate):
                    case " ", " ", " ":  # empty spot, but we expect stack here
                        if len(stacks) <= i:  # we will initialise stack with a deque
                            stacks.append(deque())
                    case "[", crate_mark, "]":  # we have a crate
                        if len(stacks) <= i:  # we will initialise stack with a deque
                            stacks.append(deque())
                        stacks[i].append(crate_mark)
        return cls(tuple(stacks))

    def __len__(self):
        return len(self._stacks)

    def __getitem__(self, index: int):
        return self._stacks[index]


class TestCreateStacksArea(unittest.TestCase):
    def test_empty_input_should_return_empty_stacks_area(self):
        stacks_area = StacksArea.from_string("")
        self.assertEqual(0, len(stacks_area))

    def test_empty_stack_should_be_marked_with_number(self):
        stacks_area = StacksArea.from_string("   \n 1 ")
        self.assertEqual(1, len(stacks_area))
        self.assertEqual(0, len(stacks_area[0]))

    def test_one_stack_with_one_crate(self):
        stacks_area = StacksArea.from_string("[S]\n 1 ")
        self.assertEqual(1, len(stacks_area))
        self.assertEqual(1, len(stacks_area[0]))
        self.assertEqual("S", stacks_area[0][0])

    def test_one_stack_with_two_crates(self):
        stacks_area = StacksArea.from_string("[S]\n[T]\n 1 ")
        self.assertEqual(1, len(stacks_area))
        self.assertEqual(2, len(stacks_area[0]))
        self.assertEqual("S", stacks_area[0][0])
        self.assertEqual("T", stacks_area[0][1])

    def test_two_stacks_with_one_crate_each(self):
        stacks_area = StacksArea.from_string("[S] [T]\n 1   2 ")
        self.assertEqual(2, len(stacks_area))
        self.assertEqual(1, len(stacks_area[0]))
        self.assertEqual(1, len(stacks_area[1]))
        self.assertEqual("S", stacks_area[0][0])
        self.assertEqual("T", stacks_area[1][0])

    def test_three_stacks_with_middle_one_empty(self):
        stacks_area = StacksArea.from_string("[S]        \n[T]     [U]\n 1   2   3 ")
        self.assertEqual(3, len(stacks_area))
        self.assertEqual(2, len(stacks_area[0]))
        self.assertEqual(0, len(stacks_area[1]))
        self.assertEqual(1, len(stacks_area[2]))


class OperationalError(Exception):
    pass


class Crane:
    def __init__(self):
        self._area = None

    def operate_over(self, area: StacksArea):
        self._area = area
        len(self._area)
        return self

    def execute(self, commands: list):
        if self._area is None:
            raise OperationalError("No area to operate!")
        return self


class TestCrane(unittest.TestCase):
    def test_crane_cannot_operate_without_area(self):
        crane = Crane()
        with self.assertRaises(OperationalError):
            crane.execute(commands=[])

    def test_crane_with_empty_commands_should_do_nothing(self):
        crane = Crane()
        area = StacksArea((["X"], [], ["Y", "Z"]))
        assert_area = deepcopy(area)
        crane.operate_over(area).execute(commands=[])
        self.assertEqual(assert_area, area)
