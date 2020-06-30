from iconservice import *
from .tokens.IRC2burnable import IRC2Burnable
from .tokens.IRC2mintable import IRC2Mintable
from .tokens.IRC2 import IRC2

TAG = 'SampleToken'

# An interface of tokenFallback.
# Receiving SCORE that has implemented this interface can handle
# the receiving or further routine.
class TokenFallbackInterface(InterfaceScore):
	@interface
	def tokenFallback(self, _from: Address, _value: int, _data: bytes):
		pass


class SampleToken(IRC2):

	@eventlog(indexed=3)
	def Transfer(self, _from: Address, _to: Address, _value: int, _data: bytes):
		pass

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)

	def on_install(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18) -> None:
		super().on_install(_tokenName, _symbolName, _initialSupply, _decimals)

	def on_update(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18) -> None:
		super().on_update(_tokenName, _symbolName, _initialSupply, _decimals)

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
	
	@external
	def balanceOf(self, account:Address) -> int:
		return super().balanceOf(account)

	@external
	def transfer(self, _to:Address, _value:int) -> bool:
		return super().transfer(_to, _value)

	@external
	def burn(self, _account:Address, _amount:int) -> None:
		return super()._burn(_account, _amount)

	@external
	def mint(self, _value:int):
		return super().mint(_value)