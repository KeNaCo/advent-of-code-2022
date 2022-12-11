import unittest


def find_compartment_overlap(bag: str) -> set[str]:
    return set()


class TestCompartmentOverlap(unittest.TestCase):
    def test_overlap_of_an_empty_bag(self):
        self.assertEqual(set(), find_compartment_overlap(bag=""))
