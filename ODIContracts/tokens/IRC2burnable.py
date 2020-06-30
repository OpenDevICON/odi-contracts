from iconservice import *
from .IRC2 import IRC2

class IRC2Burnable(IRC2):

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)

	def on_install(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18) -> None:
		super().on_install(_tokenName, _symbolName, _initialSupply, _decimals)

	def on_update(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18) -> None:
		super().on_update(_tokenName, _symbolName, _initialSupply, _decimals)

	@external
	def burn(self, _amount: int):
		# _burn is from IRC2
		super()._burn(self.address, _amount)

	# @external
	# def burnFrom(self, _account: Address, _amount: int) -> None:
	#	 self._decreasedAllowance = allowance(_account, sub(msg.sender, _amount))

	#	 #these are from IRC2
	#	 super()._approve(_account, msg.sender, self._decreasedAllowance)
	#	 super()._burn(_account, _amount)

	@external(readonly=True)
	def name(self) -> str:
		return super().name()

	@external(readonly=True)
	def symbol(self) -> str:
		return super().symbol()

	@external(readonly=True)
	def decimals(self) -> str:
		return super().decimals()

	@external(readonly=True)
	def totalSupply(self) -> int:
		return super().totalSupply()