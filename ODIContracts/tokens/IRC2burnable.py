from iconservice import *
from .IRC2 import IRC2
from ..math.SafeMath import SafeMath

class IRC2Burnable(IRC2):

	@external
	def burn(self, _amount: int) -> None:
		# _burn is from IRC2
		super()._burn(self.msg.sender, _amount)

	@external
	def burnFrom(self, _account: Address, _amount: int) -> None:
		self._decreasedAllowance = allowance(_account, SafeMath.sub(self.msg.value, _amount))

		 #these are from IRC2
		super()._approve(_account, self.msg.sender, self._decreasedAllowance)
		super()._burn(_account, _amount)
