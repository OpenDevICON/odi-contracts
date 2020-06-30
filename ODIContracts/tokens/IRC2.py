from iconservice import *
from .IIRC2 import TokenStandard
from  ..math.SafeMath import SafeMath

TAG = 'IRC_2'

class InsufficientBalanceError(Exception):
	pass

class ZeroValueError(Exception):
	pass

class InsufficientBalanceError(Exception):
	pass

class InvalidNameError(Exception):
	pass

class InvalidAccountError(Exception):
	pass

# An interface of tokenFallback.
# Receiving SCORE that has implemented this interface can handle
# the receiving or further routine.
class TokenFallbackInterface(InterfaceScore):
	@interface
	def tokenFallback(self, _from: Address, _value: int, _data: bytes):
		pass


class IRC2(TokenStandard, IconScoreBase):
	_NAME = 'name'
	_SYMBOL = 'symbol'
	_DECIMALS = 'decimals'
	_TOTAL_SUPPLY = 'total_supply'
	_BALANCES = 'balances'
	_ALLOWANCES = 'allowances'

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)

		self._name = VarDB(self._NAME, db, value_type=str)
		self._symbol = VarDB(self._SYMBOL, db, value_type=str)
		self._decimals = VarDB(self._DECIMALS, db, value_type=int)

		self._total_supply = VarDB(self._TOTAL_SUPPLY, db, value_type=int)
		self._balances = DictDB(self._BALANCES, db, value_type=int)
		self._allowances = DictDB(self._ALLOWANCES,db,value_type=int,depth=2)

	def on_install(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18) -> None:
		super().on_install()

		if (len(_symbolName) <= 0):
			raise InvalidNameError("Invalid Symbol name")
			pass
		if (len(_tokenName) <= 0):
			raise InvalidNameError("Invalid Token Name")
			pass
		if _initialSupply <= 0:
			raise ZeroValueError("Initial Supply cannot be less than zero")
			pass
		if _decimals < 0:
			raise ZeroValueError("Decimals cannot be less than zero")
			pass

		total_supply = SafeMath.mul(_initialSupply, 10 ** _decimals)

		Logger.debug(f'on_install: total_supply={total_supply}', TAG)

		self._name.set(_tokenName)
		self._symbol.set(_symbolName)
		self._total_supply.set(total_supply)
		self._decimals.set(_decimals)
		self._balances[self.msg.sender] = total_supply

	def on_update(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = 18) -> None:
		super().on_install()

		if (len(_symbolName) <= 0):
			raise InvalidNameError("Invalid Symbol name")
			pass
		if (len(_tokenName) <= 0):
			raise InvalidNameError("Invalid Token Name")
			pass
		if _initialSupply <= 0:
			raise ZeroValueError("Initial Supply cannot be less than zero")
			pass
		if _decimals < 0:
			raise ZeroValueError("Decimals cannot be less than zero")
			pass

		total_supply = SafeMath.mul(_initialSupply, 10 ** _decimals)

		Logger.debug(f'on_install: total_supply={total_supply}', TAG)

		self._name.set(_tokenName)
		self._decimals.set(_decimals)
		self._symbol.set(_symbolName)
		self._total_supply.set(total_supply)
		self._balances[self.msg.sender] = total_supply

	@external(readonly=True)
	def name(self) -> str:
		return self._name.get()

	@external(readonly=True)
	def symbol(self) -> str:
		return self._symbol.get()

	@external(readonly=True)
	def decimals(self) -> str:
		return self._decimals.get()

	@external(readonly=True)
	def totalSupply(self) -> int:
		return self._total_supply.get()

	@external
	def balanceOf(self,account: Address) -> int:
		return self._balances[account]

	@eventlog(indexed=3)
	def Transfer(self, _from: Address, _to:  Address, _value:  int, _data:  bytes): 
		pass

	@external
	def transfer(self, _to: Address, _value: int, _data: bytes = None):
		if _data is None:
			_data = b'None'
		self._transfer(self.msg.sender, _to, _value, _data)

	def _transfer(self, _from: Address, _to: Address, _value: int, _data: bytes):

		# Checks the sending value and balance.
		if _value < 0:
			revert("Transferring value cannot be less than zero")
		if self._balances[_from] < _value:
			revert("Out of balance")

		self._balances[_from] = self._balances[_from] - _value
		self._balances[_to] = self._balances[_to] + _value

		if _to.is_contract:
			# If the recipient is SCORE,
			#   then calls `tokenFallback` to hand over control.
			recipient_score = self.create_interface_score(_to, TokenFallbackInterface)
			recipient_score.tokenFallback(_from, _value, _data)

		# Emits an event log `Transfer`
		self.Transfer(_from, _to, _value, _data)
		Logger.debug(f'Transfer({_from}, {_to}, {_value}, {_data})', TAG)

	def _Nottransfer(self, _from: Address, _to: Address, _value: int, _data: bytes) -> None:
		if _value <= 0 :
			raise ZeroValueError("Transferring value cannot be less than 0.")
			return
		if self._balances[_from] < _value :
			raise InsufficientBalanceError("Insufficient balance.")
			return

		self._beforeTokenTransfer(_from, _to, _value)

		self._balances[_from] = SafeMath.sub(self._balances[_from], _value)
		self._balances[_to] = SafeMath.add(self._balances[_to], _value)

		if _to.is_contract:
			# If the recipient is SCORE,
			#   then calls `tokenFallback` to hand over control.
			recipient_score = self.create_interface_score(_to, TokenFallbackInterface)
			recipient_score.tokenFallback(_from, _value, _data)

		# Emits an event log `Transfer`
		self.Transfer(_from, _to, _value, _data)
		Logger.debug(f'Transfer({_from}, {_to}, {_value}, {_data})', TAG)

	@external
	def _mint(self, account:Address, value:int) -> bool:
		if not account.is_contract:
			raise InvalidAccountError("Invalid account address")
			pass

		if value <= 0:
			raise LessThanOrZero("Invalid Value")
			pass

		self._beforeTokenTransfer(0, account, value )

		self._total_supply = SafeMath.add(self._total_supply, value)
		self._balances[account] = SafeMath.add(self._balances[account], value)

	@external
	def _burn(self, account: Address, value: int) -> None:
		if not account.is_contract:
			raise InvalidAccountError("Invalid account address")
			pass

		# if value <= 0:
		# 	raise LessThanOrZero("Invalid Value")
		# 	pass

		self._beforeTokenTransfer(account, 0, value)

		self._total_supply = SafeMath.sub(self._total_supply, value)
		self._balances[account] = SafeMath.sub(self._balances[account], value)

	@external
	def _beforeTokenTransfer(self, _from: Address, _to: Address,_value: int) -> None:
		pass

	@external
	def _allowance(self, owner: Address, spender: Address) -> int:
		if not owner.is_contract or not spender.is_contract:
			raise InvalidAccountError("Invalid account address")
			pass

		return self._allowances[owner][spender]

	@external
	def approve(self, spender: Address, amount: int) -> bool:
		if not owner.is_contract or not spender.is_contract:
			raise InvalidAccountError("Invalid account address")
			pass

		self._approve(self.msg.sender, spender, amount)
		return true

	def _approve(self, owner:Address, spender:Address, value:int) -> None:
		self._allowances[owner][spender] = value

	@external
	def increaseAllowance(self, spender: Address, value: int) -> bool:
		self._approve(self.msg.sender, spender,  self._allowances[msg.sender][spender] + value)
		return True

	@external
	def decreaseAllowance(self, spender: Address, value: int) -> bool:
		self._approve(self.msg.sender, spender, self._allowances[msg.sender][spender] - value)
		return True
