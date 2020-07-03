from iconservice import *
# from .tokens.IRC2burnable import IRC2Burnable
from .tokens.IRC2mintable import IRC2Mintable
# from .tokens.IRC2capped import IRC2Capped
# from .tokens.IRC2pausable import IRC2Pausable
from .tokens.IRC2 import IRC2

TAG = 'SampleToken'

class SampleToken(IRC2Mintable):
	pass