from iconservice import *
from .IRC16 import *
from ...utils.pausable import *

class IRC16Pausable(IRC16):

	@eventlog(indexed=1)
	def Paused(self, status:bool):
		pass

	@external(readonly=True)
	def paused(self) -> bool:
		return self._paused.get()

	@external
	@whenNotPaused
	def pause(self):
		self._paused.set(True)
		self.Paused(True)

	@external
	@whenPaused
	def unpause(self):
		self._paused.set(False)
		self.Paused(False)

	@whenNotPaused
	def _beforeTokenTransfer(self, _from:Address, _to:Address, _amount:int) -> None:
		super()._beforeTokenTransfer(_from, _to, _amount)
