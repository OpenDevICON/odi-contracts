from iconservice import *
from ...utils.checks import *
from ...utils.consts import *
from ..roles import Roles

class PauserRole(Roles):

    @eventlog(indexed=0)
    def PauserAdded(self, _account: Address): 
        pass

    @eventlog(indexed=0)
    def PauserRemoved(self, _account: Address): 
        pass

    @external
    def isPauser(self, _account: Address) -> bool:
        return super().has(PAUSER , _account)

    @external
    def pausersList(self):
        return super()._pausersList()

    @only_owner
    @external
    def addPauser(self, _account: Address) -> bool:
        self._addPauser(_account)
        return True

    @only_owner
    @external
    def removePauser(self, _account: Address) -> bool:
        self._removePauser(_account)
        return True

    @external
    @only_pauser
    def renouncePauser(self) -> bool:
        self._removePauser(self.msg.sender)
        return True

    def _addPauser(self, _account: Address) -> None:
        super().add(PAUSER, _account)
        self.PauserAdded(_account)

    def _removePauser(self, _account: Address) -> None:
        super().remove(PAUSER, _account)
        self.PauserRemoved(_account)
