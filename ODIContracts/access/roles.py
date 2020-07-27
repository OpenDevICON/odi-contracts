from iconservice import *
from ..utils.consts import *

roles = [MINTER, BURNER, PAUSER]

class Roles(IconScoreBase):
    _ROLES = 'roles'
    _MINTERS_LIST = 'minters_list'
    _BURNERS_LIST = 'burners_list'
    _PAUSERS_LIST = 'pausers_list'

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._roles = DictDB(self._ROLES, db, value_type=bool, depth=2)
        self._minters_list = ArrayDB(self._MINTERS_LIST, db, value_type=Address)
        self._burners_list = ArrayDB(self._BURNERS_LIST, db, value_type=Address)
        self._pausers_list = ArrayDB(self._PAUSERS_LIST, db, value_type=Address)

    def on_install(self) -> None:
        super().on_install()
        self._minters_list.put(self.owner)
        self._burners_list.put(self.owner)
        self._pausers_list.put(self.owner)

    def on_update(self) -> None:
        super().on_update()

    def add(self, Role: str, _account: Address):
        if Role in roles:
            if self._roles[Role][_account]:
                revert("Selected role is already assigned to the given account.")
            self._roles[Role][_account] = True
            if Role == roles[0]:
                self._minters_list.put(_account)
            if Role == roles[1]:
                self._burners_list.put(_account)
            if Role == roles[2]:
                self._pausers_list.put(_account)

    def remove(self, Role: str, _account: Address):
        if Role in roles:
            if _account == self.owner:
                revert("Owner cannot be removed from the roles.")

            if self._roles[Role][_account]:
                self._roles[Role][_account] = False
            else:
                revert("Selected role was not assigned to the given account.")

            if Role == roles[0]:
                if _account in self._minters_list: 
                    top = self._minters_list.pop()
                    if top != _account:
                        for i in range(len(self._minters_list)):
                            if self._minters_list[i] == _account:
                                self._minters_list[i] = top
            if Role == roles[1]:
                if _account in self._burners_list: 
                    top = self._burners_list.pop()
                    if top != _account:
                        for i in range(len(self._burners_list)):
                            if self._burners_list[i] == _account:
                                self._burners_list[i] = top
            if Role == roles[2]:
                if _account in self._pausers_list: 
                    top = self._pausers_list.pop()
                    if top != _account:
                        for i in range(len(self._pausers_list)):
                            if self._pausers_list[i] == _account:
                                self._pausers_list[i] = top

    def has(self, Role: str, _account: Address) -> bool:
        if Role in roles:
            return self._roles[Role][_account]

    def _mintersList(self):
        new_list = []
        for i in range(len(self._minters_list)):
            new_list.append(self._minters_list[i])
        return new_list

    def _burnersList(self):
        new_list = []
        for i in range(len(self._burners_list)):
            new_list.append(self._burners_list[i])
        return new_list

    def _pausersList(self):
        new_list = []
        for i in range(len(self._pausers_list)):
            new_list.append(self._pausers_list[i])
        return new_list