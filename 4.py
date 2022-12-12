from dataclasses import dataclass
import unittest


@dataclass
class SectionRange:
    start: int  # included
    stop: int  # included

    def __contains__(self, item: "SectionRange") -> bool:
        pass


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
