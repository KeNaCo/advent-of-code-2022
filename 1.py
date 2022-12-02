import unittest
from typing import Sequence


def read_elf(list_of_calories: Sequence[str]) -> tuple[int]:
    elf_bag = []
    for item in list_of_calories:
        if item == '':  # end of elfs bag
            yield tuple(elf_bag)
            elf_bag = []
        elf_bag.append(int(item))


class ReadOneElfAtATimeTestCase(unittest.TestCase):
    def test_all_elfs_are_already_dead_should_return_empty_bag(self):
        list_of_calories = []
        with self.assertRaises(StopIteration):
            next(read_elf(list_of_calories))

    def test_one_elf_is_still_alive_but_has_empty_bag(self):
        list_of_calories = [""]
        output = next(read_elf(list_of_calories))
        self.assertEqual(output, tuple())

    def test_one_elf_with_something_in_his_bag(self):
        list_of_calories = ["1000", "2000", ""]
        output = next(read_elf(list_of_calories))
        self.assertEqual(output, (1000, 2000))
