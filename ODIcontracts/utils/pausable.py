
from iconservice import *

class AlreadyPausedException(Exception):
	pass

class AlreadyUnpausedException(Exception):
	pass

class Pausable(IconScoreBase):
	_PAUSED = 'paused'

	@eventlog(indexed=1)
	def Paused(self, by:Address):
		pass

	@eventlog(indexed=1)
	def Unpaused(self, by:Address):
		pass

	def __init__(self, db:IconScoreDatabase) -> None:
		super().__init__(db)
		self._paused = VarDB(self._PAUSED, db, value_type=str)

	def on_install(self):
		self._paused.set(False)


	# @external
	def paused(self) -> bool:
		return self._paused.get()

	def whenPaused(func):
		@wraps(func)
		def __wrapper(self:object, *args, **kwargs):
			if self.paused() != True:
				# revert('Not paused')
				raise AlreadyUnpausedException("The token is already unpaused.")
			return func(self, *args, **kwargs)
		return __wrapper

	def whenNotPaused(func):
		@wraps(func)
		def __wrapper(self:object, *args, **kwargs):
			if self.paused() == True:
				# revert(f'Already paused')
				raise AlreadyPausedException("The token is already paused.")
			return func(self, *args, **kwargs)
		return __wrapper

	@whenNotPaused
	def _pause():
		self._paused.set(True)
		self.Paused(self.msg.sender)

	@whenPaused
	def _unpause():
		self._paused.set(False)
		self.Unpaused(self.msg.sender)
