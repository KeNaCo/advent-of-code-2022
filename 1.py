import unittest
from typing import Sequence


def read_elf(input: Sequence[str]) -> tuple[int]:
    if not input:
        return tuple()


class ReadOneElfAtATimeTestCase(unittest.TestCase):
    def test_all_elfs_are_already_dead_should_return_empty_bag(self):
        input = []
        output = read_elf(input)
        self.assertEqual(output, tuple())