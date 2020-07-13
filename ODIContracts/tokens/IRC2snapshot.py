from iconservice import *
from .IRC2 import IRC2
from ..utils.consts import *
	
class IRC2Snapshot(IRC2):

	_ACCOUNT_BALANCE_SNAPSHOT='account_balance_snapshot'
	_TOTAL_SUPPLY_SNAPSHOT='total_supply_snapshot'
	_CURRENT_SNAPSHOT_ID='current_snapshot_id'

	def __init__(self, db: IconScoreDatabase) -> None:
		super().__init__(db)
		self._account_balance_snapshot = DictDB(self._ACCOUNT_BALANCE_SNAPSHOT, db, value_type = int, depth = 3)
		self._total_supply_snapshot = DictDB(self._TOTAL_SUPPLY_SNAPSHOT, db, value_type = int, depth = 2)
		self._current_snapshot_id = VarDB(self._CURRENT_SNAPSHOT_ID, db, value_type = int)


	def on_install(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = DEFAULT_DECIMAL_VALUE, _paused: bool = False, _cap: int = DEFAULT_CAP_VALUE) -> None:
		super().on_install(_tokenName, _symbolName, _initialSupply, _decimals,_paused,_cap)
		self._current_snapshot_id.set(0)
		self._account_balance_snapshot[self.owner]['values'][0] = _initialSupply * 10 ** _decimals
		self._account_balance_snapshot[self.owner]['length'][0] = 1
		self._total_supply_snapshot['values'][0] = _initialSupply * 10 ** _decimals
		self._total_supply_snapshot['length'][0] = 1
		
	def on_update(self, _tokenName:str, _symbolName:str, _initialSupply:int, _decimals:int = DEFAULT_DECIMAL_VALUE,_paused: bool = False,_cap: int = DEFAULT_CAP_VALUE ) -> None:
		super().on_update(_tokenName, _symbolName, _initialSupply, _decimals,_paused,_cap)
			
	@eventlog(indexed=1)
	def Snapshot(self, _id: int) -> None:
		pass

	@external
	def snapshot(self) -> None:
		self._snapshot()

	def _snapshot(self) -> None:
		current_id = self._current_snapshot_id.get() + 1
		self._current_snapshot_id.set(current_id)
		self.Snapshot(current_id)
	

	@external(readonly=True)
	def balanceOfAt(self, _account: Address, _snapshot_id: int) -> int:
		if _snapshot_id < 0:
			revert(f'IRC2Snapshot: snapshot id is equal to or greater then Zero')
		low = 0
		high = self._account_balance_snapshot[_account]['length'][0]
		
		while (low < high):
			mid = (low + high) // 2
			if self._account_balance_snapshot[_account]['ids'][mid] > _snapshot_id:
				high = mid
			else:
				low = mid + 1 
		if self._account_balance_snapshot[_account]['ids'][0] ==  _snapshot_id:
			return self._account_balance_snapshot[_account]['values'][0]	
		elif low == 0:
			return 0
		else:
			return self._account_balance_snapshot[_account]['values'][low - 1]	


	@external(readonly=True)
	def totalSupplyAt(self, _snapshot_id: int) -> int:
		if _snapshot_id < 0:
			revert(f'IRC2Snapshot: snapshot id is equal to or greater then Zero')
		low = 0
		high = self._total_supply_snapshot['length'][0]
		
		while (low<high):
			mid = (low + high) // 2
			if self._total_supply_snapshot['ids'][mid] > _snapshot_id:
				high = mid
			else:
				low = mid + 1

		if self._total_supply_snapshot['ids'][0] ==  _snapshot_id:
			return self._total_supply_snapshot['values'][0]
		elif low == 0:
			return 0
		else:
			return self._total_supply_snapshot['values'][low - 1]	

	@external
	def transfer(self,_to: Address, _value: int, _data: bytes = None) -> None:
		self._transfer(self.msg.sender, _to, _value,_data)

	def _transfer(self, _from: Address, _to: Address, _value: int, _data) -> None:
		super()._transfer(_from,_to,_value,_data)
		self._updateAccountSnapshot(_from)
		self._updateAccountSnapshot(_to)		

	@external
	def mint(self, _amount: int) -> None:
		self._mint(self.msg.sender, _amount)

	def _mint(self, _account: Address, _value: int) -> None:
		super()._mint(_account, _value)
		self._updateAccountSnapshot(_account)
		self._updateTotalSupplySnapshot()


	@external
	def burn(self, _amount: int) -> None:
		self._burn(self.msg.sender, _amount)

	def _burn(self, _account: Address, _value: int) -> None:
		super()._burn(_account, _value)
		self._updateAccountSnapshot(_account)
		self._updateTotalSupplySnapshot()

	
	def _updateAccountSnapshot(self, _account: Address) -> None:
		current_id = self._current_snapshot_id.get()
		current_value = self.balanceOf(_account)
		length = self._account_balance_snapshot[_account]['length'][0]
		if length == 0:
			self._account_balance_snapshot[_account]['values'][length] = current_value
			self._account_balance_snapshot[_account]['length'][0] = self._account_balance_snapshot[_account]['length'][0] + 1 
			return
		else:
			last_snapshot_id = self._account_balance_snapshot[_account]['ids'][length - 1]

		if last_snapshot_id < current_id :
			self._account_balance_snapshot[_account]['ids'][length] = current_id 
			self._account_balance_snapshot[_account]['values'][length] = current_value
			self._account_balance_snapshot[_account]['length'][0] = self._account_balance_snapshot[_account]['length'][0] + 1
		else:
			self._account_balance_snapshot[_account]['values'][length - 1] = current_value

	def _updateTotalSupplySnapshot(self) -> None:
		current_id = self._current_snapshot_id.get()
		current_value = self.totalSupply()
		length = self._total_supply_snapshot['length'][0]
		if length == 0:
			self._total_supply_snapshot['values'][length] = current_value
			self._total_supply_snapshot['length'][0] = self._total_supply_snapshot['length'][0] + 1
			return
		else:
			last_snapshot_id = self._total_supply_snapshot['ids'][length - 1]

		if last_snapshot_id < current_id :
			self._total_supply_snapshot['ids'][length] = current_id 
			self._total_supply_snapshot['values'][length] = current_value
			self._total_supply_snapshot['length'][0] = self._total_supply_snapshot['length'][0] + 1
		else:
			self._total_supply_snapshot['values'][length - 1] = current_value
