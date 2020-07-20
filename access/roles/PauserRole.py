from iconservice import *
from ...utils.checks import *
from ..roles import Roles

class PauserRole(IconScoreBase):
    _PAUSERS = 'pausers'

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._pausers = VarDB(self._ROLE, db, value_type=str)

    def on_install(self) -> None:
        super().on_install()
        self._pausers.set("Pauser")

    def on_update(self) -> None:
        super().on_update()

    @eventlog(indexed=0)
    def PauserAdded(self, _account: Address): 
        pass

    @eventlog(indexed=0)
    def PauserRemoved(self, _account: Address): 
        pass

    @external
    def isPauser(self, _account: Address) -> bool:
        return Roles.has(_pausers , _account)

    @only_owner
    def addPauser(self, _account: Address) -> bool:
        self._addPauser(_account)
        return True

    @only_owner
    def removePauser(self, _account: Address) -> bool:
        self._removePauser(_account)
        return True

    def renouncePauser(self) -> bool:
        self._removePauser(self.msg.sender)
        return True

    def _addPauser(self, _account: Address) -> None:
        Roles.add(_pausers, _account)
        self.PauserAdded(_account)

    def _removePauser(self, _account: Address) -> None:
        Roles.remove(_pausers, _account)
        self.PauserRemoved(_account)
