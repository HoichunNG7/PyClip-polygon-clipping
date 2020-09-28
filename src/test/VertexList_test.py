import unittest

from VertexList import VertexList


class VertexListTest(unittest.TestCase):
    def test_find_crossing_of_segments(self):
        v_list = VertexList()
        self.assertEqual(v_list.find_crossing_of_segments(0, 0, 4, 3, 0, 2, 2, 0), (8/7, 6/7))
        self.assertEqual(v_list.find_crossing_of_segments(1, 1, 3, 2, 3, 2, -1, 3), (3, 2))
        self.assertEqual(v_list.find_crossing_of_segments(2, 1, 6, -13, -2, -1, 4, 2), (2, 1))
        self.assertEqual(v_list.find_crossing_of_segments(1, 3, 5, 3, -1, -1, -3, 2), None)
        self.assertEqual(v_list.find_crossing_of_segments(-1, 17, 3, -11, 2, -3, 2, 7), (2, -4))
        self.assertEqual(v_list.find_crossing_of_segments(3, 2, 0, 0, 2, 1, 5, 0), None)
        self.assertEqual(v_list.find_crossing_of_segments(-4, 2, -7, -17, 0, -1, -3, 9), None)
        self.assertEqual(v_list.find_crossing_of_segments(3, -10, 6, -22, 7, -30, 2, 5), (17/3, -62/3))
