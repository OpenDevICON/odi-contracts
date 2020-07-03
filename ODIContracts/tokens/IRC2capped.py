from iconservice import *
from .IRC2 import IRC2
from ..math.SafeMath import SafeMath

class ZeroValueError(Exception):
	pass

class OverCapLimit(Exception):
	pass

class IRC2Capped(IRC2):
	'''
	Implementation of IRC2Capped
	'''
	
	_CAP = 'cap'

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)
		self._cap = VarDB(self._CAP, db, value_type=int)

	def on_install(self, _tokenName:str, _symbolName:str, _initialSupply:int, _cap:int, _decimals:int = 18) -> None:
		if _cap < 0:
			raise ZeroValueError("Decimals cannot be less than zero")
			pass

		if _initialSupply >= _cap:
			raise OverCapLimit("Over cap limit")
			pass

		total_cap = SafeMath.mul(_cap, 10 ** _decimals)
		self._cap.set(total_cap)
		super().on_install(_tokenName, _symbolName, _initialSupply, _decimals)

	def on_update(self, _tokenName:str, _symbolName:str, _initialSupply:int, _cap:int, _decimals:int = 18) -> None:
		if _cap < 0:
			raise ZeroValueError("Decimals cannot be less than zero")
			pass

		if _initialSupply >= _cap:
			raise OverCapLimit("Over cap limit")
			pass

		total_cap = SafeMath.mul(_cap, 10 ** _decimals)
		self._cap.set(total_cap)
		super().on_update(_tokenName, _symbolName, _initialSupply, _decimals)

	@external(readonly=True)
	def cap(self) -> str:
		'''
		Returns the cap amount.
		'''
		return self._cap.get()

	@external
	def _beforeTokenTransfer(self, _from:Address, _to:Address, _value:int) -> None:
		'''
		Checks if the total supply exceeds `cap` limit
		
		See {IRC2-_beforeTokenTransfer}
		'''
		if (self._total_supply.get() >= self._cap.get()) :
			raise OverCapLimit("IRC2 cap exceeded!")
			pass

		super()._beforeTokenTransfer(_from, _to, _value)