import unittest
import filecmp
import os
from solution import Solution

class TestIsValidCigar(unittest.TestCase):
    def test_invalid_strings(self):
        self.assertFalse(Solution.is_valid_cigar(""))
        self.assertFalse(Solution.is_valid_cigar("1"))
        self.assertFalse(Solution.is_valid_cigar("M"))
        self.assertFalse(Solution.is_valid_cigar("0M"))
        self.assertFalse(Solution.is_valid_cigar("123456789"))
        self.assertFalse(Solution.is_valid_cigar("MM"))
        self.assertFalse(Solution.is_valid_cigar("MIDNSHP=X"))

    def test_valid_cigars(self):
        self.assertTrue(Solution.is_valid_cigar("1M"))
        self.assertTrue(Solution.is_valid_cigar("1I"))
        self.assertTrue(Solution.is_valid_cigar("1D"))
        self.assertTrue(Solution.is_valid_cigar("1N"))
        self.assertTrue(Solution.is_valid_cigar("1S"))
        self.assertTrue(Solution.is_valid_cigar("1H"))
        self.assertTrue(Solution.is_valid_cigar("1P"))
        self.assertTrue(Solution.is_valid_cigar("1="))
        self.assertTrue(Solution.is_valid_cigar("1X"))
        self.assertTrue(Solution.is_valid_cigar("10M"))

        self.assertTrue(Solution.is_valid_cigar("10M"))
        self.assertTrue(Solution.is_valid_cigar("123456789M"))
        self.assertTrue(Solution.is_valid_cigar("8M7D6M2I2M11D7M"))

class TestMakeIndexMap(unittest.TestCase):
    def test_min_base_cases(self):
        self.assertEqual(Solution.make_index_map(0, "1M"), [0])
        self.assertEqual(Solution.make_index_map(0, "1I"), [0])
        self.assertEqual(Solution.make_index_map(0, "1D"), [])
        self.assertEqual(Solution.make_index_map(0, "1N"), [])
        self.assertEqual(Solution.make_index_map(0, "1S"), [0])
        self.assertEqual(Solution.make_index_map(0, "1H"), [])
        self.assertEqual(Solution.make_index_map(0, "1P"), [])
        self.assertEqual(Solution.make_index_map(0, "1="), [0])
        self.assertEqual(Solution.make_index_map(0, "1X"), [0])

    def test_max_base_cases(self):
        self.assertEqual(Solution.make_index_map(0, "10M"), [i for i in range(10)])
        self.assertEqual(Solution.make_index_map(0, "10I"), [0 for _ in range(10)])
        self.assertEqual(Solution.make_index_map(0, "10D"), [])
        self.assertEqual(Solution.make_index_map(0, "10N"), [])
        self.assertEqual(Solution.make_index_map(0, "10S"), [0 for _ in range(10)])
        self.assertEqual(Solution.make_index_map(0, "10H"), [])
        self.assertEqual(Solution.make_index_map(0, "10P"), [])
        self.assertEqual(Solution.make_index_map(0, "10="), [i for i in range(10)])
        self.assertEqual(Solution.make_index_map(0, "10X"), [i for i in range(10)])

    def test_offset(self):
        self.assertEqual(Solution.make_index_map(1, "1M"), [1])
        self.assertEqual(Solution.make_index_map(1, "10M"), [i for i in range(1,11)])

    def test_invitae_example(self):
        self.assertEqual(Solution.make_index_map(3, "8M7D6M2I2M11D7M"),
                         [3,4,5,6,7,8,9,10,18,19,20,21,22,23,24,24,24,25,37,38,39,40,41,42,43])
    def test_wikipedia_example(self):
        self.assertEqual(Solution.make_index_map(5, "3M1I3M1D5M"),
                         [5,6,7,8,8,9,10,12,13,14,15,16])


class TestFullSolution(unittest.TestCase):
    def test_invitae_full_solution(self):
        input_file_1 = "test/input_1.txt"
        input_file_2 = "test/input_2.txt"
        output_file = "test/output.txt"
        if os.path.exists(output_file):
            os.remove(output_file)
        Solution.solve(input_file_1, input_file_2, output_file)
        self.assertTrue(filecmp.cmp("test/output_ref.txt", "test/output.txt"))

if __name__ == '__main__':
    unittest.main()

