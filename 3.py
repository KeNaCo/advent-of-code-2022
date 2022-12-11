import unittest
from itertools import chain
from string import ascii_lowercase, ascii_uppercase
from typing import Sequence


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
        self.assertListEqual(["b", "a", "A"], list(scan_bags_for_errors(bags=["abcbef", "BaADEaFA", "ABCDEFG"])))
