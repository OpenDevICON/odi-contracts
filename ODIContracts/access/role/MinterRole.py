from iconservice import *
from ...utils.checks import *
from ...utils.consts import *
from ..roles import Roles

class MinterRole(Roles):

    @eventlog(indexed=0)
    def MinterAdded(self, _account: Address): 
        pass

    @eventlog(indexed=0)
    def MinterRemoved(self, _account: Address): 
        pass

    @external
    def isMinter(self, _account: Address) -> bool:
        return super().has(MINTER , _account)

    @external
    def mintersList(self):
        return super()._mintersList()

    @only_owner
    @external
    def addMinter(self, _account: Address) -> bool:
        self._addMinter(_account)
        return True

    @only_owner
    @external
    def removeMinter(self, _account: Address) -> bool:
        self._removeMinter(_account)
        return True

    @external
    @only_minter
    def renounceMinter(self) -> bool:
        self._removeMinter(self.msg.sender)
        return True

    def _addMinter(self, _account: Address) -> None:
        super().add(MINTER, _account)
        self.MinterAdded(_account)

    def _removeMinter(self, _account: Address) -> None:
        super().remove(MINTER, _account)
        self.MinterRemoved(_account)