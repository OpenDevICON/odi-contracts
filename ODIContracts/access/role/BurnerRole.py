from iconservice import *
from ...utils.checks import *
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
        super().has("burner" , _account)

    @only_owner
    def addBurner(self, _account: Address) -> bool:
        self._addBurner(_account)
        return True

    @only_owner
    def removeBurner(self, _account: Address) -> bool:
        self._removeBurner(_account)
        return True

    def renounceBurner(self) -> bool:
        self._removeBurner(self.msg.sender)
        return True

    def _addBurner(self, _account: Address) -> None:
        super().add("burner", _account)
        self.BurnerAdded(_account)

    def _removeBurner(self, _account: Address) -> None:
        super().remove("burner", _account)
        self.BurnerRemoved(_account)
