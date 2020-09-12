from iconservice import *
from .IRC3 import IRC3
from ...access.roles import Roles
from ...utils.checks import *
from ...utils.pausable import *

class IRC3Pausable(IRC3):

	@eventlog(indexed=1)
	def Paused(self, status:bool):
		pass

	@external(readonly=True)
	def paused(self) -> bool:
		return super().paused()

	@external
	@whenNotPaused
	@only_pauser
	def pause(self):
		self._paused.set(True)
		self.Paused(True)

	@external
	@whenPaused
	@only_pauser
	def unpause(self):
		self._paused.set(False)
		self.Paused(False)

	@whenNotPaused
	def _beforeTokenOperation(self, _from:Address, _to:Address, _tokenId:int):
		super()._beforeTokenOperation(_from, _to, _tokenId)