import unittest
from typing import Iterator
from unittest.mock import patch, mock_open


def read_elf(list_of_calories: Iterator[str]) -> Iterator[tuple[int]]:
    elf_bag = []
    for item in list_of_calories:
        if item == '':  # end of elfs bag
            yield tuple(elf_bag)
            elf_bag = []
            continue
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

    def test_one_elf_with_something_the_second_with_empty_bag(self):
        list_of_calories = ["1000", "", ""]
        elf_reader = read_elf(list_of_calories)
        output = next(elf_reader)
        self.assertEqual(output, (1000,))
        output = next(elf_reader)
        self.assertEqual(output, tuple())

    def test_two_elfs_with_full_bags(self):
        list_of_calories = ["1000", "", "1000", "2000", ""]
        elf_reader = read_elf(list_of_calories)
        output = next(elf_reader)
        self.assertEqual(output, (1000,))
        output = next(elf_reader)
        self.assertEqual(output, (1000, 2000))


def heaviest_bag_calories(elf_reader: Iterator[tuple[int]]) -> int:
    return max(map(sum, elf_reader))


class HeaviestCaloriesContentTestCase(unittest.TestCase):
    def test_one_elf_should_have_heaviest_bag(self):
        def mock_bag_generator() -> Iterator[tuple[int]]:
            yield 1000, 2000

        calories = heaviest_bag_calories(mock_bag_generator())
        self.assertEqual(calories, 3000)

    def test_get_the_heaviest_bag_of_many_elfs(self):
        def mock_bag_generator() -> Iterator[tuple[int]]:
            yield 1000, 2000
            yield 2000, 2000

        calories = heaviest_bag_calories(mock_bag_generator())
        self.assertEqual(calories, 4000)


def read_list_of_calories_from_file(file_name: str) -> Iterator[str]:
    with open(file_name, "rt") as file:
        return (line[:-1] for line in file.readlines())  # we strip the newline character


class ReadListOfCaloriesFromFileTestCase(unittest.TestCase):
    def test_read_list_of_calories_from_empty_file(self):
        with patch(f"{__name__}.open", mock_open(read_data="")) as m:
            list_of_calories = read_list_of_calories_from_file(file_name="1.in")
        m.assert_called_once_with("1.in", "rt")
        self.assertEqual([], list(list_of_calories))

    def test_read_list_of_calories_from_file(self):
        with patch(f"{__name__}.open", mock_open(read_data="1000\n2000\n\n1000\n\n")) as m:
            list_of_calories = read_list_of_calories_from_file(file_name="1.in")
        m.assert_called_once_with("1.in", "rt")
        self.assertEqual(["1000", "2000", "", "1000", ""], list(list_of_calories))


def top_three_heaviest_calories(elf_reader: Iterator[tuple[int]]) -> int:
    elf_bag = map(sum, elf_reader)
    # prime the list with first 3 items, we need them sorted to simplify comparison logic
    first, second, third = sorted((next(elf_bag), next(elf_bag), next(elf_bag)), reverse=True)
    for bag in elf_bag:
        if bag > first:
            third = second
            second = first
            first = bag
        elif bag > second:
            third = second
            second = bag
        elif bag > third:
            third = bag
    return first + second + third


class HeaviestTopTreeCaloriesContentTestCase(unittest.TestCase):
    def test_we_have_only_thre_elfs_left(self):
        def mock_bag_generator() -> Iterator[tuple[int]]:
            yield 1000,
            yield 2000,
            yield 3000,

        calories = top_three_heaviest_calories(mock_bag_generator())
        self.assertEqual(6000, calories)

    def test_new_heaviest_should_roll_whole_list(self):
        def mock_bag_generator() -> Iterator[tuple[int]]:
            yield 1000,
            yield 2000,
            yield 3000,  # 3 2 1
            yield 2000, 2000  # 4 3 2

        calories = top_three_heaviest_calories(mock_bag_generator())
        self.assertEqual(9000, calories)

    def test_the_second_heaviest_should_keep_first(self):
        def mock_bag_generator() -> Iterator[tuple[int]]:
            yield 1000,
            yield 2000,
            yield 5000,  # 5 2 1
            yield 3000,  # 5 3 2

        calories = top_three_heaviest_calories(mock_bag_generator())
        self.assertEqual(10000, calories)

    def test_the_third_heaviest_should_replace_only_the_last(self):
        def mock_bag_generator() -> Iterator[tuple[int]]:
            yield 3000,
            yield 1000,
            yield 5000,  # 5 3 1
            yield 2000,  # 5 3 2

        calories = top_three_heaviest_calories(mock_bag_generator())
        self.assertEqual(10000, calories)


if __name__ == '__main__':
    print("Heaviest calories:", heaviest_bag_calories(read_elf(read_list_of_calories_from_file("1.in"))))
    print("Sum of three heaviest calories:", top_three_heaviest_calories(read_elf(read_list_of_calories_from_file("1.in"))))

