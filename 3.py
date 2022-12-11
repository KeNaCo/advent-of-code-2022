import unittest
from itertools import chain
from string import ascii_lowercase, ascii_uppercase


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
