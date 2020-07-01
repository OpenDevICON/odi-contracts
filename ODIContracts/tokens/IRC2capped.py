from iconservice import *
from .IRC2 import IRC2
from ..math.SafeMath import SafeMath

class ZeroValueError(Exception):
	pass

class OverCapLimit(Exception):
	pass

class IRC2Capped(IRC2):
	_CAP = 'cap'

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)
		self._cap = VarDB(self._CAP, db, value_type=int)
		self._total_cap = VarDB(self._TOTAL_CAP, db, value_type=int)

	def on_install(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18, _cap: int) -> None:
		if _cap < 0:
			raise ZeroValueError("Decimals cannot be less than zero")
			pass

		total_cap = SafeMath.mul(_cap, 10 ** _decimals)
		self._cap.set(total_cap)

		super().on_install(_tokenName, _symbolName, _initialSupply, _decimals)

	def on_update(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18, _cap) -> None:
		if _cap < 0:
			raise ZeroValueError("Decimals cannot be less than zero")
			pass

		total_cap = SafeMath.mul(_cap, 10 ** _decimals)
		self._cap.set(total_cap)

		super().on_update(_tokenName, _symbolName, _initialSupply, _decimals)

	@external(readonly=True)
	def cap(self) -> str:
		return self._cap.get()

	@external
	def _beforeTokenTransfer(_from:Address, _to:Address, _value:int) -> None:
		super()._beforeTokenTransfer(_from, _to, _value)

		if (self._total_supply.get() >= self._cap.get()) :
			raise OverCapLimit("IRC2 cap exceeded!")
			pass
