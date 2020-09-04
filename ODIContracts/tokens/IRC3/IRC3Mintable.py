from iconservice import *
from .IRC3 import IRC3
from ...access.roles import Roles

class IRC3Mintable(IRC3, Roles):
    '''
    Implementation of IRC3Mintable
    '''

    @external
    def mint(self, _name: str, _others: str) -> None:
        super()._mint(_name, _others)