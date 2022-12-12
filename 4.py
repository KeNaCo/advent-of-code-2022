from dataclasses import dataclass
import unittest
from unittest.mock import patch, mock_open


@dataclass
class SectionRange:
    start: int  # included
    stop: int  # included

    def __contains__(self, item: "SectionRange") -> bool:
        is_in = (item.start >= self.start) and (item.stop <= self.stop)
        return is_in

    def __and__(self, other: "SectionRange") -> bool:
        dont_intersect = (other.stop < self.start) or (self.stop < other.start)
        return not dont_intersect


class TestSectionInOperator(unittest.TestCase):
    def test_distinct_ranges_should_return_false(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(3, 4)
        result = section1 in section2
        self.assertFalse(result)

    def test_intersecting_ranges_should_still_return_false(self):
        section1 = SectionRange(1, 3)
        section2 = SectionRange(2, 5)
        result = section1 in section2
        self.assertFalse(result)

    def test_one_range_inside_other_but_same_edge_should_return_true(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(1, 3)
        result = section1 in section2
        self.assertTrue(result)

    def test_one_range_inside_other_but_not_touching_the_edge_should_return_true(self):
        section1 = SectionRange(3, 3)
        section2 = SectionRange(1, 5)
        result = section1 in section2
        self.assertTrue(result)

    def test_one_range_inside_other_but_operation_is_opposite_should_return_false(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(1, 3)
        result = section2 in section1
        self.assertFalse(result)

    def test_one_range_is_the_same_as_other_should_return_true(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(1, 2)
        result = section1 in section2
        self.assertTrue(result)


class TestIntersectionOperator(unittest.TestCase):
    def test_distinct_ranges_should_return_false(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(3, 4)
        result = section1 & section2
        self.assertFalse(result)

    def test_distinct_ranges_should_return_false2(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(3, 4)
        result = section2 & section1
        self.assertFalse(result)

    def test_intersecting_ranges_should_return_true(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(2, 3)
        result = section1 & section2
        self.assertTrue(result)

    def test_intersecting_ranges_should_return_true2(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(2, 3)
        result = section2 & section1
        self.assertTrue(result)

    def test_equal_ranges_should_return_true(self):
        section1 = SectionRange(1, 2)
        result = section1 & section1
        self.assertTrue(result)

    def test_subset_ranges_should_return_true(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(1, 3)
        result = section1 & section2
        self.assertTrue(result)

    def test_superset_ranges_should_return_true(self):
        section1 = SectionRange(1, 2)
        section2 = SectionRange(1, 3)
        result = section2 & section1
        self.assertTrue(result)


def load_section_ranges_from_file(file_name: str) -> list[tuple[SectionRange, SectionRange]]:
    lines = None
    with open(file_name, "rt") as file:
        lines = file.read().splitlines()
    ranges = []
    for line in lines:  # "1-2,3-4"
        r1, r2 = line.split(",")  # "1-2", "3-4"
        r1_start, r1_stop = r1.split("-")  # "1", "2"
        r2_start, r2_stop = r2.split("-")  # "3", "4"
        ranges.append((SectionRange(int(r1_start), int(r1_stop)), SectionRange(int(r2_start), int(r2_stop))))
    return ranges


class TestLoadingSectionRangesFromFile(unittest.TestCase):
    def test_load_a_range_pair(self):
        with patch(f"{__name__}.open", mock_open(read_data="2-4,6-8\n2-3,4-5")) as m:
            result = load_section_ranges_from_file(file_name="4.in")
        m.assert_called_once_with("4.in", "rt")
        expected_result = [(SectionRange(2, 4), SectionRange(6, 8)), (SectionRange(2, 3), SectionRange(4, 5))]
        self.assertListEqual(expected_result, result)


if __name__ == "__main__":
    containing_pairs = sum(map(lambda r: (r[0] in r[1]) or (r[1] in r[0]), load_section_ranges_from_file("4.in")))
    print("Sum of containing pairs: ", containing_pairs)
