from iconservice import *

class Roles(IconScoreBase):

    _ROLE = 'role'

    def __init__(self, db: IconScoreDatabase) -> None:
        self._role = DictDB(self._ROLE, db, value_type=bool, depth=2)

    def add(self, role, _account: Address):
        if self._role[role][_account]:
            revert("Selected role is already assigned to the given account.")
        self._role[role][_account] = True

    def remove(self, role, _account: Address):
        if self._role[role][_account]:
            self._role[role][_account] = False
        else:
            revert("This account doesn't have the selected role to remove.")

    def has(self, role, _account: Address) -> bool:
        return self._role[role][_account]
