from iconservice import *
from .IRC2 import IRC2
from ..math.SafeMath import SafeMath

class IRC2Mintable(IRC2):

	@external
	def mint(self, _amount: int) -> None:
		'''
		Creates `_amount` number of tokens, and assigns to caller account.
		Increases the balance of that account and total supply.
		See {IRC2-_mint}

		:param _amount: Number of tokens to be created at the account.
		'''
		super()._mint(self.msg.sender, _amount)

	@external
	def mintTo(self, _account: Address, _amount: int) -> None:
		'''
		Creates `_amount` number of tokens, and assigns to `_account`.
		Increases the balance of that account and total supply.
		See {IRC2-_mint}

		:param _account: The account at whhich token is to be created.
		:param _amount: Number of tokens to be created at the account.
		'''
		self._increasedAllowance = self._allowance(_account, SafeMath.add(self.msg.value, _amount))

		super()._approve(_account, self.msg.sender, self._increasedAllowance)
		super()._mint(_account, _amount)
