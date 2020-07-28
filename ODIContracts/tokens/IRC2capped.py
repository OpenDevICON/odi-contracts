from iconservice import *
from .IRC2 import IRC2


class ZeroValueError(Exception):
	pass

class OverCapLimit(Exception):
	pass

class IRC2Capped(IRC2):
	'''
	Implementation of IRC2Capped
	'''

	@external(readonly=True)
	def cap(self) -> str:
		'''
		Returns the cap amount.
		'''
		return self._cap.get()


	# @external
	def _beforeTokenTransfer(self, _from:Address, _to:Address, _value:int) -> None:
		'''
		Checks if the total supply exceeds `cap` limit
		
		See {IRC2-_beforeTokenTransfer}
		'''
		if ((self._total_supply.get() + _value) >= self._cap.get()) :
			raise OverCapLimit("IRC2 cap exceeded!")
			pass

		super()._beforeTokenTransfer(_from, _to, _value)

