from iconservice import *


class Roles(IconScoreBase):

    _ROLES = 'roles'

    def __init__(self, db: IconScoreDatabase) -> None:
        self._roles = DictDB(self._ROLES, db, value_type=bool, depth=2)

    def add(Role: str, _account: Address):
        if self._roles[Role][_account]:
            revert("Selected role is already assigned to the given account.")
        self._roles[Role][_account] = True

    def remove(Role, _account: Address):
        if self._roles[Role][_account]:
            self._roles[Role][_account] = False

    def has(Role, _account: Address) -> bool:
        return self._roles[Role][_account]
