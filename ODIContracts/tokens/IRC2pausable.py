from iconservice import *
from .IRC2 import *
from ..utils.checks import *

class AlreadyPausedException(Exception):
	pass

class AlreadyUnpausedException(Exception):
	pass

class IRC2Pausable(IRC2):
	_PAUSED = 'paused'

	@eventlog(indexed=1)
	def Paused(self, by:Address):
		pass

	@eventlog(indexed=1)
	def Unpaused(self, by:Address):
		pass

	def __init__(self, db:IconScoreDatabase) -> None:
		super().__init__(db)
		self._paused = VarDB(self._PAUSED, db, value_type=bool)

	def on_install(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18, _paused:bool = False) -> None:
		self._paused.set(_paused)
		super().on_install(_tokenName, _symbolName, _initialSupply, _decimals)

	def on_update(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18, _paused:bool = False) -> None:
		self._paused.set(_paused)
		super().on_update(_tokenName, _symbolName, _initialSupply, _decimals)

	@external(readonly=True)
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

	@external
	@whenNotPaused
	def burn(self, _amount: int) -> bool:
		super()._burn(self.msg.sender, _amount)
		return True

	@external
	@whenNotPaused
	def mint(self, _amount:int) -> bool:
		super()._mint(self.msg.sender, _amount)
		return True