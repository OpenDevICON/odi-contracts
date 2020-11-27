from iconservice import *
from .IRC2 import IRC2
from ...access.roles import Roles

class IRC2Burnable(IRC2, Roles):
	'''
	Implementation of IRC2Burnable
	'''

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
		Destroys `_amount` number of tokens from the specified `_account` account
		If `self.msg.sender` is approved by `_acccount`.
		Decreases the balance of that account and total supply.
		See {IRC2-_burn}

		:param _account: The account at which token is to be destroyed.
		:param _amount: Number of tokens to be destroyed at the `_account`.
		'''
		if (self._allowance(_account, self.msg.sender) <= 0):
			revert(f"{self.msg.sender} not approved by {_account}.")

		if (self._allowance(_account, self.msg.sender) < _amount):
			revert(f"Only {_amount} was approved to {self.msg.sender}.")

		decreasedAllowance = self._allowance(_account, self.msg.sender) - _amount

		super()._approve(_account, self.msg.sender, decreasedAllowance)
		super()._burn(_account, _amount)
