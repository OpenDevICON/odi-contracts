from iconservice import *
from .IIRC16 import TokenStandard
from ...utils.consts import *
from ...utils.pausable import *

TAG = 'IRC16'

class IRC16(IconScoreBase):

    _NAME = 'name'
    _SYMBOL = 'symbol'
    _DECIMALS = 'decimals'
    _TOTAL_SUPPLY = 'total_supply'
    _BALANCES = 'balances'
    _ALLOWANCES = 'allowances'
    _PAUSED = 'paused'
    _CAP = 'cap'
    _CONTROLLABLE = "controllable"
    _CONTROLLERS = "controllers"
    _IS_CONTROLLER = "is_controller"
    _PARTITIONS = 'partitions'
    _APPROVALS = "approvals"
    _PARTITION_APPROVALS = "partition_approvals"
    _DOCUMENT = 'document'
    _ZERO_ADDRESS = Address.from_prefix_and_int(AddressPrefix.EOA, 0)

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._name = VarDB(self._NAME, db, value_type=str)
        self._symbol = VarDB(self._SYMBOL, db, value_type=str)
        self._decimals = VarDB(self._DECIMALS, db, value_type=int)
        self._total_supply = VarDB(self._TOTAL_SUPPLY, db, value_type=int)
        self._balances = DictDB(self._BALANCES, db, value_type=int)
        self._paused = VarDB(self._PAUSED, db, value_type=bool)
        self._cap = VarDB(self._CAP, db, value_type=int)
        self._controllable = VarDB(self._CONTROLLABLE, db, value_type=bool)
        self._is_controller = DictDB(self._IS_CONTROLLER, db, value_type=bool)
        self._controllers = ArrayDB(self._CONTROLLERS,db, value_type=Address)
        self._partitions = DictDB(self._PARTITIONS, db, value_type=int, depth=2)
        self._document = DictDB(self._DOCUMENT, db, value_type=str, depth=2)
        self._approvals = DictDB(self._APPROVALS, db, value_type=bool, depth = 2)
        self._partition_approvals = DictDB(self._PARTITION_APPROVALS, db, value_type=bool, depth = 3)

    def on_install(self, _name:str, _symbol:str, _initialSupply:int, _decimals:int, _paused: bool = False, _cap: int = DEFAULT_CAP_VALUE, _controllable: bool = True) -> None:
        super().on_install()
        if (len(_symbol) <= 0):
            revert("Invalid Symbol name")
        if (len(_name) <= 0):
            revert("Invalid Token Name")
        if _initialSupply <= 0:
            revert("Initial Supply cannot be less than zero")
        if _decimals < 0:
            revert("Decimals cannot be less than zero")
        if _cap <= 0:
            revert("Cap value cannot be less than zero")
        if _cap < _initialSupply:
            revert("Cap value cannot be less than initial supply")
        total_supply = _initialSupply * 10 ** _decimals

        self._name.set(_name)
        self._symbol.set(_symbol)
        self._decimals.set(_decimals)
        self._total_supply.set(total_supply)
        self._cap.set(_cap)
        self._paused.set(_paused)

        self._controllable.set(_controllable)
        self._controllers.put(self.owner)

    def on_update(self) -> None:
        super().on_update()

    # Eventlogs
    @eventlog(indexed=2)
    def TransferByPartition(self, _partition: str, _operator: Address, _from: Address, _to: Address, _amount: int, _data: bytes):
        pass

    @eventlog(indexed=3)
    def IssueByPartition(self, _partition: str, _to: Address, _amount: int, _data: bytes):
        pass

    @eventlog(indexed=3)
    def RedeemByPartition(self, _partition: str, _operator: Address, _owner: Address, _amount: int, _data: bytes):
        pass

    @eventlog(indexed=2)
    def AuthorizeOperator(self, _operator: Address, _sender: Address):
        pass

    @eventlog(indexed=2)
    def RevokeOperator(self, _operator: Address, _sender: Address):
        pass

    @eventlog(indexed=3)
    def AuthorizeOperatorForPartition(self, _owner: Address, _partition: str, _operator: Address):
        pass

    @eventlog(indexed=3)
    def RevokeOperatorForPartition(self, _owner: Address, _partition: str, _operator: Address):
        pass

    @eventlog(indexed=3)
    def SetDocument(self, _name: str, _uri: str, _document_hash: str):
        pass

    @external(readonly=True)
    def name(self) -> str:
        return self._name.get()

    @external(readonly=True)
    def symbol(self) -> str:
        return self._symbol.get()

    @external(readonly=True)
    def decimals(self) -> int:
        return self._decimals.get()

    @external(readonly=True)
    def totalSupply(self) -> int:
        return self._total_supply.get()

    @external(readonly=True)
    def balanceOf(self, _owner: Address) -> int:
        return self._balances[_owner]

    @external(readonly=True)
    def balanceOfByPartition(self, _partition: str, _owner: Address) -> int:
        return self._partitions[_owner][_partition]

    # @external(readonly=True)
    # def partitionsOf(self, _owner: Address) -> DictDB:
    #     return self._partitions[_owner]

    @external(readonly=True)
    def getDocument(self, _name:str) -> dict:
        doc = {}
        doc = {
            "name" : _name,
            "uri" : self._document[_name]['uri'],
            "document_hash" : self._document[_name]['document_hash'],
        }
        return doc

    @external
    def setDocument(self, _name: str, _uri: str, _document_hash: str) -> None:
        if (self.msg.sender != self.owner):
            revert("Only self.owner has permission to set document.")
        self._document[_name]['uri'] = _uri
        self._document[_name]['document_hash'] = _document_hash
        self.SetDocument(_name, _uri, _document_hash)

    @external(readonly=True)
    @whenNotPaused
    def canTransferByPartition(self, _partition: str, _to: Address, _amount: int, _data: bytes = None) -> str:
        if _to == self._ZERO_ADDRESS:
            revert("ZERO ADDRESS: Invalid Recieving Address")
        elif self._partitions[_from][_partition] < _amount:
            revert("Insufficient partition balance.")
        elif self._balances[_from] < _amount:
            revert("Insufficient balance.")
        elif not self._partitions[_from][_partition]: 
            revert("Invalid partition")

        return "Transfer can be successful."

    @external
    def transferByPartition(self, _partition: str, _to: Address, _amount: int, _data: bytes = None) -> None:
        self._transferByPartition(_partition, self.msg.sender,self.msg.sender, _to, _amount, _data)

    @external
    def operatorTransferByPartition(self, _partition: str, _from: Address, _to: Address, _amount: int, _data: bytes = None) -> None:
        if self.isOperatorForPartition(_partition, self.msg.sender, _from) or self.isOperator(self.msg.sender, _from):
            self._transferByPartition(_partition, self.msg.sender, _from, _to, _amount, _data)
        else:
            revert(f"{self.msg.sender} is not a operator.")

    def _transferByPartition(self, _partition: str,_operator: Address, _from: Address, _to: Address, _amount: int, _data:bytes = None) -> None:
        if self._partitions[_from][_partition] < _amount:
            revert("Insufficient partition balance.")
        if self._balances[_from] < _amount:
            revert("Insufficient balance.")

        self._beforeTokenTransfer(_from, _to, _amount)

        self._partitions[_from][_partition] -= _amount
        self._balances[_from] -= _amount
        self._partitions[_to][_partition] += _amount
        self._balances[_to] += _amount
        self.TransferByPartition(_partition, _operator, _from, _to, _amount, _data)

    @external
    def authorizeOperator(self, _operator: Address) -> None:
        if self._approvals[self.msg.sender][_operator]:
            revert(f"{_operator} is already a operator.")
        self._approvals[self.msg.sender][_operator] = True
        self.AuthorizeOperator(_operator, self.msg.sender)

    @external
    def revokeOperator(self, _operator: Address) -> None:
        if not self._approvals[self.msg.sender][_operator]:
            revert(f"{_operator} is not a operator.")
        self._approvals[self.msg.sender][_operator] = False
        self.RevokeOperator(_operator, self.msg.sender)

    @external
    def authorizeOperatorForPartition(self, _partition: str, _operator: Address) -> None:
        if self._partition_approvals[self.msg.sender][_partition][_operator]:
            revert(f"{_operator} is already a operator for {_partition} partition.")
        self._partition_approvals[self.msg.sender][_partition][_operator] = True
        self.AuthorizeOperatorForPartition(self.msg.sender, _partition, _operator)

    @external
    def revokeOperatorForPartition(self, _partition: str, _operator: Address) -> None:
        if not self._partition_approvals[self.msg.sender][_partition][_operator]:
            revert(f"{_operator} is already not a operator for {_partition} partition.")
        self._partition_approvals[self.msg.sender][_partition][_operator] = False
        self.AuthorizeOperatorForPartition(self.msg.sender, _partition, _operator)

    @external(readonly=True)
    def isOperator(self, _operator: Address, _owner: Address) -> bool:
        return self._approvals[_owner][_operator]

    @external(readonly=True)
    def isOperatorForPartition(self, _partition: str, _operator: Address, _owner: Address) -> bool:
        return self._partition_approvals[_owner][_partition][_operator]

    @external
    def issueByPartition(self, _partition: str, _to: Address, _amount: int, _data: bytes) -> None:
        if self.msg.sender != self.owner:
            revert("Only owner has permission.")

        self._beforeTokenTransfer(self._ZERO_ADDRESS, _to, _amount)

        new_balance = self._total_supply.get() + _amount
        self._total_supply.set(new_balance)
        self._balances[_to] += _amount
        self._partitions[_to][_partition] += _amount
        self.IssueByPartition(_partition, _to, _amount, _data)

    @external
    def redeemByPartition(self, _partition: str, _from: Address, _amount: int, _data: bytes) -> None:
        if self.msg.sender != self.owner:
            revert("Only owner has permission.")
        if self._partitions[_from][_partition] < _amount:
            revert(f"{_from} does not have suffifient partition amount.")

        self._beforeTokenTransfer(_from, self._ZERO_ADDRESS, _amount)

        new_balance = self._total_supply.get() - _amount
        self._total_supply.set(new_balance)
        self._balances[_to] -= _amount
        self._partitions[_to][_partition] -= _amount
        self.RedeemByPartition(_partition, self.msg.sender, _to, _amount, _data)

    def _addController(self, _account: Address):
        if (self.msg.owner != self.owner):
            revert("No permission to add controllers.")
        self._is_controller[_account] = True
        self._controllers.put(_account)

    def _removeController(self, _account):
        if _account == self.owner:
            revert("Owner cannot be removed from the roles.")
        if not self._is_controller[_account]:
            revert(f"{_account} is not a controller.")
        self._is_controller[_account] = False
        if _account in self._controllers: 
            top = self._controllers.pop()
            if top != _account:
                for i in range(len(self._controllers)):
                    if self._controllers[i] == _account:
                        self._controllers[i] = top

    def _beforeTokenTransfer(self, _from: Address, _to: Address, _amount: int) -> None:
        pass 