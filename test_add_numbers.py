import unittest
import sys
from add_numbers import add_numbers, parse_input

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(5, 3), 8.0)
        self.assertEqual(add_numbers(-5, 3), -2.0)
        self.assertEqual(add_numbers(0, 0), 0.0)
    
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(2.5, 3.7), 6.2)
        self.assertAlmostEqual(add_numbers(-2.5, 3.7), 1.2)
        self.assertAlmostEqual(add_numbers(0.1, 0.2), 0.3)
    
    def test_add_mixed_types(self):
        self.assertEqual(add_numbers(4, 2.5), 6.5)
        self.assertEqual(add_numbers(2.5, 4), 6.5)
    
    def test_overflow_protection(self):
        # Test with numbers close to float max
        max_float = sys.float_info.max
        self.assertRaises(OverflowError, add_numbers, max_float, max_float)
        self.assertRaises(OverflowError, add_numbers, -max_float, -max_float)
    
    def test_invalid_input(self):
        self.assertRaises(TypeError, add_numbers, "5", 3)
        self.assertRaises(TypeError, add_numbers, 5, "3")
        self.assertRaises(TypeError, add_numbers, None, 3)
        self.assertRaises(TypeError, add_numbers, 5, None)

class TestParseInput(unittest.TestCase):
    def test_valid_input(self):
        self.assertEqual(parse_input("5"), 5.0)
        self.assertEqual(parse_input("3.14"), 3.14)
        self.assertEqual(parse_input("-2.5"), -2.5)
    
    def test_invalid_input(self):
        self.assertRaises(ValueError, parse_input, "abc")
        self.assertRaises(ValueError, parse_input, "")
        self.assertRaises(ValueError, parse_input, "1.2.3")

if __name__ == '__main__':
    unittest.main() 