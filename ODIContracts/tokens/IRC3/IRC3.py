from iconservice import *
from .IIRC3 import TokenStandard
from ...utils.checks import *

TAG = 'IRC3'

class IRC3(IconScoreBase, TokenStandard):
    '''
    Implementation of IRC3
    '''
    _PAUSED = 'paused'
    _TOKENS_LIST = "tokens_list"
    _TOKEN_OWNER = "get_tokens_of_owner"
    _OWNED_TOKEN_COUNT = 'owned_token_count'  # Track token count against token owners
    _TOKEN_APPROVALS = "token_approvals"
    _TOKEN = "TOKEN"
    _ZERO_ADDRESS = Address.from_prefix_and_int(AddressPrefix.EOA, 0)

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

        self._paused = VarDB(self._PAUSED, db, value_type=bool)
        self._tokenList = ArrayDB(self._TOKENS_LIST, db, value_type=int)
        self._ownedTokenCount = DictDB(self._OWNED_TOKEN_COUNT, db, value_type=int)
        self._tokenOwner = DictDB(self._TOKEN_OWNER, db, value_type=Address)
        self._tokenApprovals = DictDB(self._TOKEN_APPROVALS, db, value_type=Address)
        self._token = DictDB(self._TOKEN, db, depth=1, value_type=str)

    def on_install(self, _paused: bool = False) -> None:
        super().on_install()
        self._paused.set(_paused)

    def on_update(self) -> None:
        super().on_update()
    
    @external(readonly=True)
    def name(self) -> str:
        return "IRC3 Token"

    @external(readonly=True)
    def symbol(self) -> str:
        return "IRC3"

    @external(readonly=True)
    def totalSupply(self) -> int:
        return len(self._tokenList)

    @external(readonly=True)
    def balanceOf(self, _owner: Address) -> int:
        if _owner is None or self._is_zero_address(_owner):
            revert("Invalid owner")
        return self._ownedTokenCount[_owner]

    @external(readonly=True)
    def ownerOf(self, _tokenId: int) -> Address:
        self.is_valid(_tokenId)
        owner = self._tokenOwner[_tokenId]
        if owner is None:
            revert("Invalid _tokenId: Token with that id does not exist.")
        if self._is_zero_address(owner):
            revert("Invalid _tokenId: Token with that id was burned.")
        return owner

    @external(readonly=True)
    def getApproved(self, _tokenId: int) -> Address:
        self.is_valid(_tokenId)
        addr = self._tokenApprovals[_tokenId]
        if addr is None:
            return self._ZERO_ADDRESS
        return addr

    @external(readonly=True)
    def getToken(self, _tokenId:int) -> dict:
        self.is_valid(_tokenId)
        token = self._load_token(_tokenId)
        return token

    @eventlog(indexed=3)
    def Transfer(self, _from: Address, _to: Address, _tokenId: int):
        pass

    @eventlog(indexed=3)
    def Approval(self, _from: Address, _to: Address, _tokenId: int):
        pass

    @eventlog(indexed=1)
    def Mint(self, _tokenId:int):
        pass

    @eventlog(indexed=1)
    def Update(self, _tokenId:int):
        pass

    @eventlog(indexed=1)
    def Burn(self, _tokenId:int):
        pass

    @external
    def approve(self, _to:Address, _tokenId:int):
        owner = self.ownerOf(_tokenId)
        if _to == owner:
            revert("Cannot approve to yourself.")
        if self.msg.sender != owner:
            revert(" You do not own this token.")
        self._tokenApprovals[_tokenId] = _to
        self.Approval(owner, _to, _tokenId) 

    @external
    def clear_approval(self, _tokenId:int):
        owner = self.ownerOf(_tokenId)
        if self.getApproved(_tokenId) == self._ZERO_ADDRESS:
            revert("Token has not been approved.")
        if self.msg.sender != owner:
            revert("You do not have permission to clear approval.")
        del self._tokenApprovals[_tokenId]

    @external
    def transfer(self, _to: Address, _tokenId: int):        
        if self.msg.sender != self.ownerOf(_tokenId):
            revert("Only token owner can transfer tokens.")
        self._transfer(self.msg.sender, _to, _tokenId)

    @external
    def transferFrom(self, _from: Address, _to: Address, _tokenId: int):
        owner = self.ownerOf(_tokenId)
        if owner != _from:
            revert("_from does not own this token.")
        if self.msg.sender != self._tokenApprovals[_tokenId] and self.msg.sender != owner:
            revert("Only approved addresses can transfer.")
        self._transfer(_from, _to, _tokenId)

    def paused(self) -> bool:
        return self._paused.get()

    def _transfer(self, _from: Address, _to: Address, _tokenId: int):
        self.is_valid(_tokenId)
        self._beforeTokenOperation(_from, _to, _tokenId)

        if _to is None or self._is_zero_address(_to):
            revert("Cannot transfer tokens to zero address.")

        del self._tokenApprovals[_tokenId]

        self._tokenOwner[_tokenId] = _to
        self._ownedTokenCount[_from] -= 1
        self._ownedTokenCount[_to] += 1

        self.Transfer(_from, _to, _tokenId)

    @only_minter
    def _mint(self, _name:str, _others:str):
        attribs = {
            'name': _name,
            'others': _others
        }
        _tokenId = int(self.totalSupply() + 1)
        self._beforeTokenOperation(0, self.msg.sender, _tokenId)
        self._ownedTokenCount[self.msg.sender] += 1 
        self._tokenList.put(_tokenId)
        self._tokenOwner[_tokenId] = self.msg.sender
        self._token[_tokenId] = json_dumps(attribs)
        self.Mint(_tokenId)

    @only_minter
    def _update(self, _tokenId:int, _name:str, _others:str):
        self.is_valid(_tokenId)
        self._beforeTokenOperation(0, self.msg.sender, _tokenId)
        updated_attribs = {
            'name': _name,
            'others': _others
        }
        self._token[_tokenId] = json_dumps(updated_attribs)
        self.Update(_tokenId)

    @only_burner
    def _burn(self, _tokenId):
        self.is_valid(_tokenId)
        owner = self._tokenOwner[_tokenId]
        self._beforeTokenOperation(owner, 0, _tokenId)
        self._ownedTokenCount[owner] -= 1 
        self._tokenOwner[_tokenId] = self._ZERO_ADDRESS
        del self._token[_tokenId]
        self.Burn(_tokenId)

    def is_valid(self, _tokenId:int) -> bool:
        if _tokenId not in self._tokenList:
            revert(f"{_tokenId} is not valid. Token with id {_tokenId} does not exist.")
        return True

    def _load_token(self, _tokenId:int) -> dict:
        token = {}
        token = json_loads(self._token[_tokenId])
        return token

    def _is_zero_address(self, _address: Address) -> bool:
        # Check if address is zero address
        if _address == self._ZERO_ADDRESS:
            return True
        return False

    def _beforeTokenOperation(self, _from, _to, _tokenId):
        pass