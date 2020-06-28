from iconservice import *
from .token.IRC2 import *

class Token(IRC2):
	# ================================================
	#  Initialization
	# ================================================
	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)

	def on_install(self) -> None:
		super().on_install()

	def on_update(self) -> None:
		super().on_update()