from iconservice import *
from ...utils.checks import *
from ..roles import Roles

class MinterRole(IconScoreBase):
    _MINTERS = 'minters'

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._minters = VarDB(self._ROLE, db, value_type=str)

    def on_install(self) -> None:
        super().on_install()
        self._minters.set("Minter")

    def on_update(self) -> None:
        super().on_update()

    @eventlog(indexed=0)
    def MinterAdded(self, _account: Address): 
        pass

    @eventlog(indexed=0)
    def MinterRemoved(self, _account: Address): 
        pass

    @external
    def isMinter(self, _account: Address) -> bool:
        return Roles.has(_minters , _account)

    @only_owner
    def addMinter(self, _account: Address) -> bool:
        self._addMinter(_account)
        return True

    @only_owner
    def removeMinter(self, _account: Address) -> bool:
        self._removeMinter(_account)
        return True

    def renounceMinter(self) -> bool:
        self._removeMinter(self.msg.sender)
        return True

    def _addMinter(self, _account: Address) -> None:
        Roles.add(_minters, _account)
        self.MinterAdded(_account)

    def _removeMinter(self, _account: Address) -> None:
        Roles.remove(_minters, _account)
        self.MinterRemoved(_account)
