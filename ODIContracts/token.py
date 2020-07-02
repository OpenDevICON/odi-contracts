from iconservice import *
# from .tokens.IRC2burnable import IRC2Burnable
# from .tokens.IRC2mintable import IRC2Mintable
# from .tokens.IRC2capped import IRC2Capped
# from .tokens.IRC2pausable import IRC2Pausable
from .tokens.IRC2 import IRC2

TAG = 'SampleToken'

class SampleToken(IRC2):

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)

	def on_install(self, _tokenName: str, _symbolName: str, _initialSupply: int, _decimals: int = 18) -> None:
		super().on_install(_tokenName, _symbolName, _initialSupply, _decimals)

	def on_update(self, _tokenName: str, _symbolName: str, _initialSupply: int, _decimals: int = 18,) -> None:
		super().on_update(_tokenName, _symbolName, _initialSupply, _decimals)