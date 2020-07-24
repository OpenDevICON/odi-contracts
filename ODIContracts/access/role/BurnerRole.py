from iconservice import *
from ...utils.checks import *
from ...utils.consts import *
from ..roles import Roles

class BurnerRole(Roles):

    @eventlog(indexed=0)
    def BurnerAdded(self, _account: Address): 
        pass

    @eventlog(indexed=0)
    def BurnerRemoved(self, _account: Address): 
        pass

    @external
    def isBurner(self, _account: Address) -> bool:
        return super().has(BURNER, _account)

    @external
    def burnersList(self):
        return super()._burnersList()

    @only_owner
    @external
    def addBurner(self, _account: Address) -> bool:
        self._addBurner(_account)
        return True

    @only_owner
    @external
    def removeBurner(self, _account: Address) -> bool:
        self._removeBurner(_account)
        return True

    @external
    @only_burner
    def renounceBurner(self) -> bool:
        self._removeBurner(self.msg.sender)
        return True

    def _addBurner(self, _account: Address) -> None:
        super().add(BURNER, _account)
        self.BurnerAdded(_account)

    def _removeBurner(self, _account: Address) -> None:
        super().remove(BURNER, _account)
        self.BurnerRemoved(_account)