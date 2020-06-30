from iconservice import *
# from .tokens.IRC2burnable import IRC2Burnable
# from .tokens.IRC2mintable import IRC2Mintable
from .tokens.IRC2 import IRC2

TAG = 'SampleToken'

class SampleToken(IRC2):

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)

	def on_install(self) -> None:
		super().on_install()

	def on_update(self) -> None:
		super().on_update()