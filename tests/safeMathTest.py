import unittest
from ..math/SafeMath import *

class TestSafeMath(unittest.TestCase):
	def test_add(self):
		with self.assertRaises(NegativeNumbers):
			c = SafeMath.add(-2,3)
		
		with self.assertRaises(NegativeNumbers):
			c = SafeMath.add(-2, -2)

		with self.assertRaises(NegativeNumbers):
			c = SafeMath.add(2,-2)

		c = SafeMath.add(3,3)
		self.assertEqual(c, 6)


	def test_sub(self): 
		# with self.assertRaises(NegativeNumbers):
		# 	c = SafeMath.sub(-2,-3)
		
		# with self.assertRaises(NegativeNumbers):
		# 	c = SafeMath.sub(-2, -2)

		with self.assertRaises(SubtractionOverFlowError):
			c = SafeMath.sub(1,2)

		# with self.assertRaises(SubtractionOverFlowError):
		# 	c = SafeMath.sub(2,3)
		
		c = SafeMath.sub(3,2)
		self.assertEqual(c, 1)


	def test_mul(self):
		with self.assertRaises(NegativeNumbers):
			c = SafeMath.mul(-2,3)
		
		with self.assertRaises(NegativeNumbers):
			c = SafeMath.mul(-2, -2)

		with self.assertRaises(NegativeNumbers):
			c = SafeMath.mul(2,-2)
		
		c = SafeMath.mul(3,2)
		self.assertEqual(c,6)


	def test_div(self):
		with self.assertRaises(NegativeNumbers):
			c = SafeMath.div(-2,3)
		
		with self.assertRaises(NegativeNumbers):
			c = SafeMath.div(-2, -2)

		with self.assertRaises(NegativeNumbers):
			c = SafeMath.div(2,-2)

		c = SafeMath.div(9,3)
		self.assertEqual(c, 3)
		

	def test_mod(self):
		with self.assertRaises(NegativeNumbers):
			c = SafeMath.mod(-2,3)
		
		with self.assertRaises(NegativeNumbers):
			c = SafeMath.mod(-2, -2)

		with self.assertRaises(NegativeNumbers):
			c = SafeMath.mod(2,-2)

		c = SafeMath.mod(9,3)
		self.assertEqual(c,0)
