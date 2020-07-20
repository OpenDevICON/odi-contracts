from iconservice import *
from ..utils.checks import *

roles = ["minter", "burner", "pauser"]

class Roles(IconScoreBase):
    _ROLES = 'roles'
    _MINTERS_LIST = 'minters_list'
    _BURNERS_LIST = 'burners_list'
    _PAUSERS_LIST = 'pausers_list'

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._roles = DictDB(self._ROLES, db, value_type=bool, depth=2)
        self._minters_list = ArrayDB(self._MINTERS_LIST, db, value_type=int)
        self._burners_list = ArrayDB(self._BURNERS_LIST, db, value_type=int)
        self._pausers_list = ArrayDB(self._PAUSERS_LIST, db, value_type=int)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()

    def add(Role: str, _account: Address):
        if Role in roles:
            if self._roles[Role][_account]:
                revert("Selected role is already assigned to the given account.")
            self._roles[Role][_account] = True
            if Role = roles[0]:
                self._minters_list.append(_account)
            if Role = roles[1]:
                self._burners_list.append(_account)
            if Role = roles[2]:
                self._pausers_list.append(_account)

    def remove(Role: str, _account: Address):
        if Role in roles:
            if self._roles[Role][_account]:
                self._roles[Role][_account] = False
            else:
                revert("Selected role was not assigned to the given account.")
            if Role = roles[0]:
                if _account in self._minters_list: 
                    self._minters_list.remove(_account)
            if Role = roles[1]:
                if _account in self._burners_list: 
                    self._burners_list.remove(_account)
            if Role = roles[2]:
                if _account in self._pausers_list: 
                    self._pausers_list.remove(_account)


    def has(Role: str, _account: Address) -> bool:
        if Role in roles:
            return self._roles[Role][_account]