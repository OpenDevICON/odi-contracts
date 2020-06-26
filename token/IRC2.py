from iconservice import *
import .IIRC2


TAG = 'IRC_2'

class InsufficientBalanceError(Exception):
    pass

class ZeroValueError(Exception):
    pass

class InsufficientBalanceError(Exception):
    pass


# An interface of tokenFallback.
# Receiving SCORE that has implemented this interface can handle
# the receiving or further routine.
class TokenFallbackInterface(InterfaceScore):
    @interface
    def tokenFallback(self, _from: Address, _value: int, _data: bytes):
        pass


class IRC2(IIRC2, IconScoreBase):
    _NAME = 'name'
    _SYMBOL = 'symbol'
    _DECIMAL = 'decimal'
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


    def on_install(self, _tokenName:str, _symbolName:str, _initialSupply:int, decimals:int = 18) -> None:
        super().on_install()

        if (len(_symbolName) <= 0):
            revert("invalid symbol name")
        if (len(_tokenName) <= 0):
            revert("Invalid token name")
        if _initialSupply <= 0:
            raise ZeroValueError("Initial Supply cannot be less than zero")
            pass
        if _decimals < 0:
            raise ZeroValueError("Decimals cannot be less than zero")
            pass

        Logger.debug(f'on_install: total_supply={total_supply}', TAG)

        total_supply = _initialSupply * 10 ** _decimals
        self._name.set(_tokenName)
        self._decimals.set(_decimals)
        self._symbol.set(_symbolName)
        self._balances[self.msg.sender] = total_supply

    def on_update(self) -> None:
        super().on_update()
    
    @external(readonly=True)
    def hello(self)-> str:
        Logger.debug(f'Hello, world!', TAG)
        return "Hello"

    @external(readonly=True)
    def name(self) -> str:
        return self._name.get()

    @external(readonly=True)
    def symbol(self) -> str:
        return self._symbol.get()

    @external(readonly=True)
    def decimals(self) -> str:
        return self._decimal.get()

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
    def transfer(self, _to: Address, _value: int, _data: bytes = None) -> bool:
        self._transfer(self.msg.sender, _to, _value, _data)
        return true

    def _transfer(self, _from: Address, _to: Address, _value: int, _data: bytes) -> None:
        if _value <= 0 :
            raise ZeroValueError("Transferring value cannot be less than 0.")
            return
        if self._balances[_from] < _value :
            raise InsufficientBalanceError("Insufficient balance.")
            return

        self._beforeTokenTransfer(_from, _to, _value)

        self._balances[_from] -=_value
        self._balances[_to] += _value

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
        if !account.is_contract:
            raise InvalidAccountError("Invalid account address")
            pass

        if value <= 0:
            raise LessThanOrZero("Invalid Value")
            pass

        self._beforeTokenTransfer(0, account, value )

        self._total_supply += value
        self._balances[account] += value

    @external
    def _burn(self, account: Address, value: int) -> bool:
        if !account.is_contract:
            raise InvalidAccountError("Invalid account address")
            pass

        if value <= 0:
            raise LessThanOrZero("Invalid Value")
            pass

        self._beforeTokenTransfer(account, 0, value)

        self._total_supply -= value
        self._balances[account] -= value

    @external
    def _beforeTokenTransfer(self, _from: Address, _to: Address,_value: int) -> None:
        pass

    @external
    def _allowance(self, owner: Address, spender: Address) -> int:
        if !owner.is_contract or !spender.is_contract:
            raise InvalidAccountError("Invalid account address")
            pass

        return self._allowances[owner][spender]

    @external
    def approve(self, spender: Address, amount: int) -> bool:
        if !owner.is_contract or !spender.is_contract:
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
