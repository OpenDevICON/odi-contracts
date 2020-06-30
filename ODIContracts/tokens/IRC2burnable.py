from iconservice import *
from .IRC2 import IRC2
from ..math.SafeMath import SafeMath

class IRC2Burnable(IRC2):

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)

	def on_install(self) -> None:
		super().on_install()

	def on_update(self) -> None:
		super().on_update()

	@external
	def burn(self, _amount: int) -> None:
		# _burn is from IRC2
		super()._burn(self.msg.sender, _amount)

	@external
	def burnFrom(self, _account: Address, _amount: int) -> None:
		self._decreasedAllowance = allowance(_account, SafeMath.sub(msg.sender, _amount))

		 #these are from IRC2
		super()._approve(_account, msg.sender, self._decreasedAllowance)
		super()._burn(_account, _amount)
