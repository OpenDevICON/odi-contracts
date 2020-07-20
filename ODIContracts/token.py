from iconservice import *
from .tokens.IRC2burnable import IRC2Burnable
from .tokens.IRC2mintable import IRC2Mintable
from .tokens.IRC2capped import IRC2Capped
from .tokens.IRC2pausable import IRC2Pausable
from .tokens.IRC2 import IRC2
from .access.roles import Roles
from .access.role.MinterRole import MinterRole
from .access.role.PauserRole import PauserRole

TAG = 'SampleToken'

class SampleToken(MinterRole, PauserRole):
	pass