from iconservice import *
from .IRC2 import IRC2
from ..math.SafeMath import SafeMath

class IRC2Burnable(IRC2):

	@external
	def burn(self, _amount: int) -> None:
		'''
		Destroys `_amount` number of tokens from the caller account.
		Decreases the balance of that account and total supply.
		See {IRC2-_burn}

		:param _amount: Number of tokens to be destroyed.
		'''
		super()._burn(self.msg.sender, _amount)

	@external
	def burnFrom(self, _account: Address, _amount: int) -> None:
		'''
		Destroys `_amount` number of tokens from the caller account.
		Decreases the balance of that account and total supply.
		See {IRC2-_burn}

		:param _account: The account at whhich token is to be destroyed.
		:param _amount: Number of tokens to be destroyed at the `_account`.
		'''
		self._decreasedAllowance = allowance(_account, SafeMath.sub(self.msg.value, _amount))

		super()._approve(_account, self.msg.sender, self._decreasedAllowance)
		super()._burn(_account, _amount)
