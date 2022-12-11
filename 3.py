import unittest


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
