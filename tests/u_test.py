import sys, os
sys.path.insert(0, os.path.dirname(__file__).strip('tests'))

import unittest
import mox
from coolcalc import analyzer
from coolcalc import calculator
from coolcalc import validator
from coolcalc import arithmetic
from coolcalc.handler import FileHandler
from coolcalc.storage import ExpressionStorageManagerToFile

class TestArithmetic(unittest.TestCase):

	def setUp(self):
		self.calc = arithmetic.Arithmetic()

	def tearDown(self):
		pass

	def test_add_2_to_2_give_4(self):
		self.assertEquals(4, self.calc.add(2, 2))

	def test_add_5_to_7_give_12(self):
		self.assertEquals(12, self.calc.add(5, 7))

	def test_commutative_property_is_met(self):
		self.assertEquals(self.calc.add(6, 2), 
						  self.calc.add(2, 6))

	def test_subtract_3_to_5(self):
		self.assertEquals(2, self.calc.subtract(5, 3))

	def test_subtract_3_to_2(self):
		self.assertEquals(-1, self.calc.subtract(2, 3))

	def test_commutative_property_isnt_met(self):
		self.assertNotEquals(self.calc.subtract(3, 1), 
							 self.calc.subtract(1, 3))

	def test_add_2_negative_numbers(self):
		self.assertEquals(0, self.calc.add(-2, 2))

	def test_subtract_2_negative_numbers(self):
		self.assertEquals(-7, self.calc.subtract(-5, 2))
		self.assertEquals(-5, self.calc.subtract(-7, -2))

	def test_exact_division(self): 
		self.assertEquals(1, self.calc.divide(2, 2))
		self.assertEquals(2, self.calc.divide(10, 5))

	def test_negative_exact_division(self):
		self.assertEquals(-2, self.calc.divide(10, -5))
		self.assertEquals(2, self.calc.divide(-10, -5))

	def test_no_exact_division_throws_exception(self):
		self.assertRaises(ValueError, self.calc.divide, 3, 2)

	def test_division_by_0_throws_exception(self):
		self.assertRaises(ZeroDivisionError, self.calc.divide, 3, 0)

	def test_multiply_4_by_2_give_8(self):
		self.assertEquals(8, self.calc.multiply(4, 2))

	def test_negative_multiplication(self):
		self.assertEquals(-8, self.calc.multiply(-4, 2))
		self.assertEquals(-8, self.calc.multiply(4, -2))
		self.assertEquals(8, self.calc.multiply(-4, -2))

class TestAnalyzer(unittest.TestCase):

	def setUp(self):
		self.expAnalyzer = analyzer.ExpresionAnalyser()

	def tearDown(self):
		pass

	def test_fetch_operatings_and_operators_when_add_2_to_2(self):
		self.assertEquals({'operatings': [2, 2], 
							'operators': ['+']}, 
							self.expAnalyzer.parse("2 + 2"))

	def test_fetch_operatings_and_operators_when_divide_10_by_negative_5(self):
		self.assertEquals({'operatings': [10, -5], 
							'operators': ['/']}, 
							self.expAnalyzer.parse("10 / -5"))

	def test_fetch_operatings_and_operators_of_complex_expresion_without_parenthesis(self):
		self.assertEquals({'operatings': [5, 4, 2, 2], 
							'operators': ['+', '*', '/']}, 
							self.expAnalyzer.parse("5 + 4 * 2 / 2"))

class TestCalculator(unittest.TestCase):

	def setUp(self):
		self.cool_calc = calculator.Calculator(
							analyzer.ExpresionAnalyser(),
							validator.ValidatorArithmeticExpression())
	def tearDown(self):
		pass

	def test_add(self):
		self.assertEquals("4", self.cool_calc.calculate("2 + 2"))	

	def test_subtract(self):
		self.assertEquals("0", self.cool_calc.calculate("2 - 2"))

	def test_calculate_complex_expression_without_parentheses_without_precendence(self):
		self.assertEquals("6", self.cool_calc.calculate("5 + 4 - 3"))

	def test_calculate_complex_expression_without_parentheses_with_precendence(self):
		self.assertEquals("3", self.cool_calc.calculate("5 + 4 / 2 - 4"))
		self.assertEquals("-1", self.cool_calc.calculate("4 / 2 - 3"))
		self.assertEquals("1", self.cool_calc.calculate("4 / 2 - 3 + 1 + 6 / 3 - 1"))
		self.assertEquals("-8", self.cool_calc.calculate("4 / -2 + 3 + -1 + -6 / -3 - 10"))
		self.assertEquals("9", self.cool_calc.calculate("5 + 4 * 2 / 2"))

	def test_calculate_complex_expression_all_operations_without_parentheses_with_precendence(self):
		self.assertEquals("11", self.cool_calc.calculate("4 - -3 * 2 / 3 + 5"))

	def test_calculate_invalidate_expression_throws_exception(self):
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "4 & 3")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "1 * # 8")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "* * 4 - 2")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "* % / * 4 + 2")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "4 5")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "6 8 4")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "232 4 -2")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "* 4 5 - 2")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "+ - 342 74 - 9")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "3 + 2 -3")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "3 + 4 -")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "+ 2 / 2 +")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "1 * 8 * - +")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "* + - /")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "* 4 5 - 2 - ")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "2+3-4*3/1")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "7-+5 4 * 3")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "*45-2-")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "cuatro mas 3")
		self.assertRaises(SyntaxError, self.cool_calc.calculate, "5")


	def test_calculator_using_validator(self):
		# we use a stub for this test
		validator_stub = validator.ValidatorArithmeticExpression()
		validator_mock = mox.Mox()
		validator_mock.StubOutWithMock(validator_stub, 'validate')
		validator_stub.validate("2 ^ 3").AndReturn(False)
		validator_mock.ReplayAll()
		cool_calc = calculator.Calculator(
						analyzer.ExpresionAnalyser(),
						validator_stub)
		self.assertRaises(SyntaxError, cool_calc.calculate, "2 ^ 3")
		validator_mock.UnsetStubs()
		validator_mock.VerifyAll()

class TestValidator(unittest.TestCase):

	def test_expression_is_validate(self):
		val = validator.ValidatorArithmeticExpression()
		self.assertTrue(val.validate("3 + 4"))
		self.assertTrue(val.validate("-3 + 4 * -5 / 1"))

	def test_expression_isnt_validate(self):
		val = validator.ValidatorArithmeticExpression()
		self.assertFalse(val.validate("4 & 3"))
		self.assertFalse(val.validate("* % / * 4 + 2"))

class TestExpressionStorageManager(unittest.TestCase):

	def test_the_expression_is_saved_on_sytem_file(self):
		file_hanler_stub = FileHandler()
		file_handler_mock = mox.Mox()

		file_handler_mock.StubOutWithMock(file_hanler_stub, 'save')
		file_hanler_stub.save("2 + 7;9")
		file_handler_mock.ReplayAll()

		exp_storage = ExpressionStorageManagerToFile(file_hanler_stub)
		exp_storage.insert("2 + 7", "9")

		file_handler_mock.UnsetStubs()
		file_handler_mock.VerifyAll()


if __name__ == "__main__":
	# print os.path.dirname(__file__)
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(TestArithmetic))
	suite.addTest(unittest.makeSuite(TestAnalyzer))
	suite.addTest(unittest.makeSuite(TestCalculator))
	suite.addTest(unittest.makeSuite(TestValidator))
	suite.addTest(unittest.makeSuite(TestExpressionStorageManager))
	unittest.TextTestRunner(verbosity=3).run(suite)