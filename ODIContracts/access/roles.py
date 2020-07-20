from iconservice import *
from ..utils.checks import *

roles = ["minter", "burner", "pauser"]

class Roles(IconScoreBase):
    _ROLES = 'roles'

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._roles = DictDB(self._ROLES, db, value_type=bool, depth=2)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()

    @external
    def add(Role: str, _account: Address):
        if Role in roles:
            if self._roles[Role][_account]:
                revert("Selected role is already assigned to the given account.")
            self._roles[Role][_account] = True

    @only_owner
    def remove(Role, _account: Address):
        if Role in roles:
            if self._roles[Role][_account]:
                self._roles[Role][_account] = False

    def has(Role, _account: Address) -> bool:
        if Role in roles:
            return self._roles[Role][_account]