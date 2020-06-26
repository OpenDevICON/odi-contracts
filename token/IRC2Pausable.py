from iconservice import *
from ..utils.pausable import Pausable
from .IRC2 import IRC2

class IRC2Pausable(Pausable, IRC2):

	@abstractmethod
	def _beforeTokenTransfer(self, _from:Address, _to:Address,_value:int) -> None:
		super()._beforeTokenTransfer(_from, _to, _value)

		if (super().paused()):
			revert("Token cannot be transfered while paused")