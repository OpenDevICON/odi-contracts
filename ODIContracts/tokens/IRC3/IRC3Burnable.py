from iconservice import *
from .IRC3 import IRC3
from ...access.roles import Roles

class IRC3Burnable(IRC3, Roles):
	'''
	Implementation of IRC3Burnable
	'''

	@external
	def burn(self, _tokenId: int) -> None:
		super()._burn(_tokenId)