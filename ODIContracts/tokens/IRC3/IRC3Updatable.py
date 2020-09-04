from iconservice import *
from .IRC3 import IRC3
from ...access.roles import Roles

class IRC3Updatable(IRC3, Roles):
	'''
	Implementation of IRC3Updatable
	'''

	@external
	def update(self, _tokenId: int, _name: str, _others: str) -> None:
		super()._update(_tokenId, _name, _others)