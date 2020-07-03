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
	def Paused(self, by:Address):
		pass

	@eventlog(indexed=1)
	def Unpaused(self, by:Address):
		pass

	@external(readonly=True)
	def paused(self) -> bool:
		return super().paused()

	@external
	@whenNotPaused
	@only_owner
	def pause(self):
		self._paused.set(True)
		self.Paused(self.msg.sender)

	@external
	@whenPaused
	@only_owner
	def unpause(self):
		self._paused.set(False)
		self.Unpaused(self.msg.sender)