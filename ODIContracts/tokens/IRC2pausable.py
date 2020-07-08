from iconservice import *
from .IRC2 import *
from ..utils.checks import *
from ..utils.pausable import *

class AlreadyPausedException(Exception):
	pass

class AlreadyUnpausedException(Exception):
	pass

class IRC2Pausable(IRC2):

	@eventlog(indexed=1)
	def Paused(self, status:bool):
		pass

	@external(readonly=True)
	def paused(self) -> bool:
		return super().paused()

	@external
	@whenNotPaused
	@only_owner
	def pause(self):
		self._paused.set(True)
		self.Paused(True)

	@external
	@whenPaused
	@only_owner
	def unpause(self):
		self._paused.set(False)
		self.Paused(False)

	@whenNotPaused
	@external
	def _beforeTokenTransfer(self, _from:Address, _to:Address, _value:int) -> None:
		super()._beforeTokenTransfer(_from, _to, _value)
