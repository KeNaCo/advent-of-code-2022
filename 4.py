from dataclasses import dataclass
import unittest


@dataclass
class SectionRange:
    start: int  # included
    stop: int  # included

    def __contains__(self, item: "SectionRange") -> bool:
        is_in = (item.start >= self.start) and (item.stop <= self.stop)
        return is_in


class TestSectionUseCases(unittest.TestCase):
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
