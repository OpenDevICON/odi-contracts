from iconservice import *

class AlreadyPausedException(Exception):
	pass

class AlreadyUnpausedException(Exception):
	pass

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
