from iconservice import *
from .IRC2 import IRC2

class ZeroValueError(Exception):
	pass

class OverCapLimit(Exception):
	pass

class IRC2Capped(IRC2):
	_CAP = 'cap'

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)
		self._cap = VarDB(self._CAP, db, value_type=int)

	def on_install(self, _cap:int) -> None:
		super().on_install()

		if _cap < 0:
			raise ZeroValueError("Decimals cannot be less than zero")
			pass

		self._cap.set(_cap)

	def on_update(self) -> None:
		super().on_update()

	@external(readonly=True)
	def cap(self) -> str:
		return self._cap.get()

	@external
	def _beforeTokenTransfer(_from:Address, _to:Address, _value:int) -> None:
		super()._beforeTokenTransfer(_from, _to, _value)

		if (self._total_supply >= self._cap) :
			raise OverCapLimit("IRC2 cap exceeded!")
			pass
