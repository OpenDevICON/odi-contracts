from iconservice import *
from .IRC2 import IRC2
from ..math.SafeMath import SafeMath

class IRC2Mintable(IRC2):

	@external
	def mint(self, _amount: int) -> None:
		# _burn is from IRC2
		super()._mint(self.msg.sender, _amount)

	@external
	def mintTo(self, _account: Address, _amount: int) -> None:
		self._increasedAllowance = self._allowance(_account, SafeMath.add(self.msg.value, _amount))

		 #these are from IRC2
		super()._approve(_account, self.msg.sender, self._increasedAllowance)
		super()._mint(_account, _amount)
