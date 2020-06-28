class AdditionOverFlowError(Exception):
	pass


class SubtractionOverFlowError(Exception):
	pass


class MultiplicationOverFlowError(Exception):
	pass


class DivisionByZero(Exception):
	pass


class ModulobyZeroError(Exception):
	pass


class NegativeNumbers(Exception):
	pass


class SafeMath:

	def _require_positive(*args):
		for arg in args:
			if (arg < 0):
				raise NegativeNumbers
				break

	def add(a: int, b: int) -> int:
		"""	 
		Returns the addition of two unsigned integers, reverting on
		overflow.

		Counterpart to default `+` operator.

		Requirements:
				- Addition cannot overflow.
		"""
		# _require_positive(a, b)
		if (a<0 or b<0):
			raise NegativeNumbers("Numbers cannot be negative")
			return
		c = a+b
		if (c <= a):
			raise AdditionOverFlowError("Addition overflow happened.")
			return
		else:
			return c

	def sub(a: int, b: int) -> int:
		'''
		Returns the subtraction of two unsigned integers, reverting on
		overflow (when the result is negative).

		Counterpart to default `-` operator.

		Requirements:
				- Subtraction cannot overflow.
		'''
		# _require_positive(a, b)
		if (a<0 or b<0):
			raise NegativeNumbers("Numbers cannot be negative")
			return
		if b >= a:
			raise SubtractionOverFlowError("First argument must be greater than the second.")
			return
		else:
			c = a - b
			return c

	def mul(a: int, b: int) -> int:
		"""	 
		Returns the multiplication of two unsigned integers, reverting on
		overflow.

		Counterpart to default `*` operator.

		Requirements:
				- Multiplication cannot overflow.
		"""
		# _require_positive(a, b)
		if (a<0 or b<0):
			raise NegativeNumbers("Numbers cannot be negative")
		c = a*b
		if (c//a != b):
			raise MultiplicationOverFlowError
		else:
			return c

	def div(a: int, b: int) -> int:
		"""	 
		Returns the integer division of two unsigned integers, reverting on
		division by number less than zero.

		Counterpart to default `/` operator.

		Requirements:
				- Divisor cannot be less than zero.
		"""
		# _require_positive(a, b)
		if (a<0 or b<0):
			raise NegativeNumbers("Numbers cannot be negative")
		if (b < 0):
			raise DivisionByLessThanZeroError
		c = a//b
		return c

	def mod(a: int, b: int) -> int:
		"""	 
		Returns the remainder of two unsigned integers, reverting on
		division by zero.

		Counterpart to default `%` operator.

		Requirements:
				- Divisor cannot overflow.
		"""
		# _require_positive(a, b)
		if (a<0 or b<0):
			raise NegativeNumbers("Numbers cannot be negative")
		if (b == 0):
			raise ModulobyZeroError
		else:
			c = a % b
			return c
