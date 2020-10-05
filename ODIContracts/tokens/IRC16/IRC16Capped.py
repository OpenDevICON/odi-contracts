from iconservice import *
from .IRC16 import IRC16

class IRC16Capped(IRC16):

	@external(readonly=True)
	def cap(self) -> int:
		'''
		Returns the cap amount.
		'''
		return self._cap.get()


	def _beforeTokenTransfer(self, _from:Address, _to:Address, _amount:int) -> None:
		'''
		Checks if the total supply exceeds `cap` limit
		
		See {IRC16-_beforeTokenTransfer}
		'''
		if ((self._total_supply.get() + _amount) > self._cap.get()) :
			revert("Exceeded Cap Limit.")

		super()._beforeTokenTransfer(_from, _to, _amount)

