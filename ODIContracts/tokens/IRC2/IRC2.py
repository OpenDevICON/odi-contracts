from iconservice import *
from .IIRC2 import TokenStandard
from ...utils.checks import *
from ...utils.consts import *

TAG = 'IRC2'

class InsufficientBalanceError(Exception):
    pass

class ZeroValueError(Exception):
    pass

class InvalidNameError(Exception):
    pass

class OverCapLimit(Exception):
    pass

class InsufficientAllowanceError(Exception):
    pass


# An interface of tokenFallback.
# Receiving SCORE that has implemented this interface can handle
# the receiving or further routine.
class TokenFallbackInterface(InterfaceScore):
    @interface
    def tokenFallback(self, _from: Address, _value: int, _data: bytes):
        pass


class IRC2(IconScoreBase, TokenStandard):
    '''
    Implementation of IRC2
    '''
    _NAME = 'token_name'
    _SYMBOL = 'token_symbol'
    _DECIMALS = 'decimals'
    _TOTAL_SUPPLY = 'total_supply'
    _BALANCES = 'balances'
    _ALLOWANCES = 'allowances'
    _PAUSED = 'paused'
    _CAP = 'cap'

    def __init__(self, db: IconScoreDatabase) -> None:
        '''
        Varible Definition
        '''
        super().__init__(db)

        self._name = VarDB(self._NAME, db, value_type=str)
        self._symbol = VarDB(self._SYMBOL, db, value_type=str)
        self._decimals = VarDB(self._DECIMALS, db, value_type=int)

        self._total_supply = VarDB(self._TOTAL_SUPPLY, db, value_type=int)
        self._balances = DictDB(self._BALANCES, db, value_type=int)
        self._allowances = DictDB(self._ALLOWANCES,db,value_type=int,depth=2)
        self._paused = VarDB(self._PAUSED, db, value_type=bool)
        self._cap = VarDB(self._CAP, db, value_type=int)

    def on_install(self, _name:str, _symbol:str, _initialSupply:int, _decimals:int = DEFAULT_DECIMAL_VALUE, _paused:bool = False, _cap:int=DEFAULT_CAP_VALUE) -> None:
        '''
        Variable Initialization.

        :param _tokenName: The name of the token.
        :param _symbolName: The symbol of the token.
        :param _initialSupply: The total number of tokens to initialize with. 
                    It is set to total supply in the beginning.
        :param _decimals: The number of decimals. Set to 18 by default.
        :param _paused: To check if it is paused.
        :param _cap: The max number of tokens that can be created.

        total_supply is set to `_initialSupply`* 10 ^ decimals.
        _cap is set to `_cap` * 10 ^ decimals.

        Raise 
        InvalidNameError
            If the length of strings `_symbolName` and `_tokenName` is 0 or less.
        ZeroValueError
            If `_initialSupply` is 0 or less.
            If `_cap` value is 0 or less.
            If `_decimals` value is 0 or less.
        OverCapLimit
            If `_initialSupply` is more than `_cap` value.
        '''
        super().on_install()

        if (len(_symbol) <= 0):
            raise InvalidNameError("Invalid Symbol name")
            pass
        if (len(_name) <= 0):
            raise InvalidNameError("Invalid Token Name")
            pass
        if _initialSupply <= 0:
            raise ZeroValueError("Initial Supply cannot be less than zero")
            pass
        if _decimals < 0:
            raise ZeroValueError("Decimals cannot be less than zero")
            pass
        if _cap <= 0:
            raise ZeroValueError("Cap value cannot be less than zero")
            pass
        if _cap != DEFAULT_CAP_VALUE:
            if _initialSupply >= _cap:
                raise OverCapLimit("Over cap limit")
                pass    

        total_supply = _initialSupply * 10 ** _decimals
        total_cap = _cap * 10 ** _decimals
        Logger.debug(f'on_install: total_supply={total_supply}', TAG)

        self._name.set(_name)
        self._symbol.set(_symbol)
        self._decimals.set(_decimals)
        self._total_supply.set(total_supply)
        self._balances[self.msg.sender] = total_supply
        self._paused.set(_paused)
        self._cap.set(total_cap)

    def on_update(self) -> None:
        super().on_update()

    @external(readonly=True)
    def name(self) -> str:
        '''
        Returns the name of the token 
        '''
        return self._name.get()

    @external(readonly=True)
    def paused(self) -> bool:
        '''
        Returns if the token operations are paused
        '''
        return self._paused.get()

    @external(readonly=True)
    def symbol(self) -> str:
        '''
        Returns the symbol of the token 
        '''
        return self._symbol.get()

    @external(readonly=True)
    def decimals(self) -> int:
        '''
        Returns the number of decimals
        For example, if the decimals = 2, a balance of 25 tokens 
        should be displayed to the user as (25 * 10 ** 2)

        Tokens usually opt for value of 18. It is also the IRC2 
        uses by default. It can be changed by passing required 
        number of decimals during initialization. 
        '''
        return self._decimals.get()

    @external(readonly=True)
    def totalSupply(self) -> int:
        '''
        Returns the total number of tokens in existence
        '''
        return self._total_supply.get()

    @external(readonly=True)
    def balanceOf(self, _owner: Address) -> int:
        '''
        Returns the amount of tokens owned by the account

        :param _owner: The account whose balance is to be checked.
        :return Amount of tokens owned by the `_owner` with the given address.

        >>> balanceOf(account)
         '0x12ba23423ef243'
        '''
        return self._balances[_owner]

    @eventlog(indexed=3)
    def Transfer(self, _from: Address, _to:  Address, _value:  int, _data:  bytes): 
        pass

    @eventlog(indexed=1)
    def Mint(self, account:Address, amount: int):
        pass

    @eventlog(indexed=1)
    def Burn(self, account: Address, amount: int):
        pass

    @external
    def transfer(self, _to: Address, _value: int, _data: bytes = None):
        '''
        Transfers certain amount of tokens from sender to the reciever.
        
        :param _to: The account to which the token is to be transferred.
        :param _value: The no. of tokens to be transferred.
        :param _data: Any information or message 
        '''
        if _data is None:
            _data = b'None'
        self._transfer(self.msg.sender, _to, _value, _data)    

    @external
    def _allowance(self, owner: Address, spender: Address) -> int:
        '''
        Returns the number of tokens that the `spender` will be allowed
        to spend on behalf of `owner`.

        :param owner: The account which provides the allowance.
        :param spender: The account  which recieves the allowance from the owner.
        :return The allowance amount
        '''
        return self._allowances[owner][spender]

    @external
    def approve(self, spender: Address, amount: int) -> bool:
        '''
        Returns a boolean value to check if the operation was successful

        :param spender: The account to which allowance is provided.
        :param amount: The `amount` provided to the spender as allowance.
        '''

        self._approve(self.msg.sender, spender, amount)
        return True

    @external
    def transferFrom(self, sender:Address, recepient:Address, amount:int) -> bool:
        '''
        Moves `amount` tokens from `sender` to `recipient` using the allowance mechanism.
        `amount` is then deducted from the caller's allowance.

        :param sender: The address which gives allowance.
        :param recepient: The address to which the address with the allowance   
            is to transfer the `amount`.
        :param amount: The amount to be transferred from `sender` to `recepient`.

        Raises
        InsufficientAllowanceError
        If the amount to be transferred exceeds the allowance amount.
        '''
        if (self._allowances[sender][self.msg.sender] - amount < 0):
            raise InsufficientAllowanceError("The amount exceeds the allowance")

        self._transfer(sender, recepient, amount)
        self._approve(sender, self.msg.sender, self._allowances[sender][self.msg.sender] - amount)
        return True

    @external
    def increaseAllowance(self, spender: Address, value: int) -> bool:
        '''
        Increases the allowance granted to `spender` by the caller
        Returns a boolean value if the operation was successful

        :param spender: The account which gets the allowance.
        :param value: The amount of allowance to be increased by.
        '''
        self._approve(self.msg.sender, spender, self._allowances[self.msg.sender][spender]+ value)
        return True

    @external
    def decreaseAllowance(self, spender: Address, value: int) -> bool:
        '''
        Decreases the allowance granted to `spender` by the caller
        Returns a boolean value if the operation was successful

        :param spender: The account which gets the allowance.
        :param value: The amount of allowance to be decreased by.
        '''
        self._approve(self.msg.sender, spender, self._allowances[self.msg.sender][spender] - value)
        return True

    def _transfer(self, _from: Address, _to: Address, _value: int, _data: bytes):
        '''
        Transfers certain amount of tokens from sender to the recepient.
        This is an internal function.

        :param _from: The account from which the token is to be transferred.
        :param _to: The account to which the token is to be transferred.
        :param _value: The no. of tokens to be transferred.
        :param _data: Any information or message 
        
        Raises
        ZeroValueError
            if the value to be transferrd is less than 0
        InsufficientBalanceError
            if the sender has less balance than the value to be transferred
        '''
        if _value < 0 :
            raise ZeroValueError("Transferring value cannot be less than 0.")
            return

        if _data == b'mint':
            _from = self.address

        if self._balances[_from] < _value :
            raise InsufficientBalanceError("Insufficient balance.")
            return

        self._beforeTokenTransfer(_from, _to, _value)

        self._balances[_from] -=  _value
        self._balances[_to] += _value

        if _to.is_contract:
            '''
            If the recipient is SCORE,
            then calls `tokenFallback` to hand over control.
            '''
            recipient_score = self.create_interface_score(_to, TokenFallbackInterface)
            recipient_score.tokenFallback(_from, _value, _data)

        # Emits an event log `Transfer`
        self.Transfer(_from, _to, _value, _data)
        Logger.debug(f'Transfer({_from}, {_to}, {_value}, {_data})', TAG)

    @only_minter
    def _mint(self, account:Address, amount:int) -> bool:
        '''
        Creates amount number of tokens, and assigns to account
        Increases the balance of that account and total supply.
        This is an internal function.

        :param account: The account at which token is to be created.
        :param amount: Number of tokens to be created at the `account`.

        Raises
        ZeroValueError
            if the `amount` is less than or equal to zero.
        '''

        if amount <= 0:
            raise ZeroValueError("Invalid Value")
            pass

        # self._beforeTokenTransfer(0, account, amount)

        self._total_supply.set(self._total_supply.get() + amount)
        self._balances[self.address] +=  amount
        self._transfer(self.address, account, amount, b'mint')


        # Emits an event log Mint
        self.Mint(account, amount)
        
    @only_burner
    def _burn(self, account: Address, amount: int) -> None:
        '''
        Destroys `amount` number of tokens from `account`
        Decreases the balance of that `account` and total supply.
        This is an internal function.

        :param account: The account at which token is to be destroyed.
        :param amount: The `amount` of tokens of `account` to be destroyed.

        Raises
        ZeroValueError
            if the `amount` is less than or equal to zero
        '''

        if amount <= 0:
            raise ZeroValueError("Invalid Value")
            pass

        self._beforeTokenTransfer(account, 0, amount)

        self._total_supply.set(self._total_supply.get() - amount)
        self._balances[account] -= amount
        
        # Emits an event log Burn
        self.Burn(account, amount)

    def _approve(self, owner:Address, spender:Address, value:int) -> None:
        '''
        Sets the allowance value given by the owner to the spender
        This is an internal function.
            
        See {IRC2-approve}
        :returns The allowance amount provided by `owner` to the `spender`.
        '''
        self._allowances[owner][spender] = value

    def _beforeTokenTransfer(self, _from: Address, _to: Address,_value: int) -> None:
        '''
        Called before transfer of tokens.
        This is an internal function.

        If `_from` and `_to` are both non zero, `_value` number of tokens
        of `_from` will be transferred to `_to`

        If `_from` is zero `_value` tokens will be minted to `_to`.

        If `_to` is zero `_value` tokens will be destroyed from `_from`.

        Both `_from` and `_to` are never both zero at once.
        '''
        pass 