import unittest
from itertools import chain
from string import ascii_lowercase, ascii_uppercase
from unittest.mock import patch, mock_open


def find_compartment_overlap(bag: str) -> set[str]:
    middle = len(bag) // 2
    compartment1, compartment2 = set(bag[:middle]), set(bag[middle:])
    return compartment1 & compartment2


class TestCompartmentOverlap(unittest.TestCase):
    def test_overlap_of_an_empty_bag(self):
        self.assertEqual(set(), find_compartment_overlap(bag=""))

    def test_overlap_in_bag_with_one_item(self):
        self.assertEqual(set(), find_compartment_overlap(bag="1"))

    def test_overlap_in_bag_with_more_items_without_overlap(self):
        self.assertEqual(set(), find_compartment_overlap(bag="123"))

    def test_overlap_in_bag_with_overlap_compartments(self):
        self.assertEqual({"1"}, find_compartment_overlap(bag="121"))
        self.assertEqual({"1"}, find_compartment_overlap(bag="1231"))


def build_item_priority_index() -> dict[str, int]:
    index = {item: priority for item, priority in zip(chain(ascii_lowercase, ascii_uppercase), range(1, 53))}
    return index


class TestIndexBuild(unittest.TestCase):
    def test_index_is_correct(self):
        index = build_item_priority_index()
        self.assertEqual(52, len(index))
        self.assertEqual(1, index["a"])
        self.assertEqual(52, index["Z"])


def scan_bags_for_errors(bags):
    return chain.from_iterable(filter(lambda overlaps: overlaps, map(find_compartment_overlap, bags)))


class TestScanBags(unittest.TestCase):
    def test_no_bags(self):
        self.assertEqual([], list(scan_bags_for_errors(bags=[])))

    def test_one_bag_with_overlap(self):
        self.assertEqual(["b"], list(scan_bags_for_errors(bags=["abcbd"])))

    def test_one_bag_without_overlap_should_be_filtered_out(self):
        self.assertEqual([], list(scan_bags_for_errors(bags=["abcdef"])))

    def test_multiple_bags(self):
        self.assertCountEqual(["b", "a", "A"], list(scan_bags_for_errors(bags=["abcbef", "BaADEaFA", "ABCDEFG"])))


def load_bags_from_file(file_name: str) -> list[str]:
    with open(file_name, "rt") as file:
        return file.read().splitlines()


class LoadBagsFromFile(unittest.TestCase):
    def test_load_bags_from_file(self):
        with patch(f"{__name__}.open", mock_open(read_data="abcbef\nBaADEaFA\nABCDEFG")) as m:
            result = load_bags_from_file(file_name="3.in")
        m.assert_called_once_with("3.in", "rt")
        self.assertEqual(["abcbef", "BaADEaFA", "ABCDEFG"], result)


def find_badge(bag1: str, bag2: str, bag3: str) -> set[str]:
    return set(bag1) & set(bag2) & set(bag3)


class TestBadgeItemOverlap(unittest.TestCase):
    def test_find_overlap_of_three_bags(self):
        result = find_badge(
            bag1="vJrwpWtwJgWrhcsFMMfFFhFp", bag2="jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", bag3="PmmdzqPrVvPwwTWBwg"
        )
        self.assertEqual({"r"}, result)


def group_bags(bags):
    group = []
    for bag in bags:
        group.append(bag)
        if len(group) == 3:
            yield group
            group = []


def scan_bags_for_badges(bags):
    groups = (group for group in group_bags(bags))
    return chain.from_iterable(filter(lambda overlaps: overlaps, map(lambda group: find_badge(*group), groups)))


class TEstScanBagsForBadges(unittest.TestCase):
    def test_no_bags(self):
        self.assertEqual([], list(scan_bags_for_badges(bags=[])))

    def test_two_bags_with_overlap(self):
        self.assertEqual(
            [], list(scan_bags_for_badges(bags=["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL"]))
        )

    def test_three_bags_with_overlap(self):
        result = list(
            scan_bags_for_badges(
                bags=["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg"]
            )
        )
        self.assertEqual(["r"], result)

    def test_six_bags_with_overlap(self):
        result = list(
            scan_bags_for_badges(
                bags=[
                    "vJrwpWtwJgWrhcsFMMfFFhFp",
                    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                    "PmmdzqPrVvPwwTWBwg",
                    "vJrwpWtwJgWrhcsFMMfFFhFp",
                    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                    "PmmdzqPrVvPwwTWBwg",
                ]
            )
        )
        self.assertEqual(["r", "r"], result)


if __name__ == "__main__":
    index = build_item_priority_index()
    error_items_priorities_sum = sum(map(lambda i: index[i], scan_bags_for_errors(load_bags_from_file("3.in"))))
    print("Sum of error items priorities is: ", error_items_priorities_sum)
    badge_items_prioriteis_sum = sum(map(lambda i: index[i], scan_bags_for_badges(load_bags_from_file("3.in"))))
    print("Sum of badge items priorities in: ", badge_items_prioriteis_sum)
