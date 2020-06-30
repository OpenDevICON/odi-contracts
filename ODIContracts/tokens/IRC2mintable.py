from iconservice import *
from .IRC2 import IRC2
from ..math.SafeMath import SafeMath

class IRC2Mintable(IRC2):

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)

	def on_install(self) -> None:
		super().on_install()

	def on_update(self) -> None:
		super().on_update()

	@external
	def mint(self, _amount: int) -> None:
		# _burn is from IRC2
		super()._mint(self.msg.sender, _amount)

	@external
	def mintTo(self, _account: Address, _amount: int) -> None:
		 self._increasedAllowance = allowance(_account, SafeMath.add(msg.sender, _amount))

		 #these are from IRC2
		 super()._approve(_account, msg.sender, self._increasedAllowance)
		 super()._mint(_account, _amount)
