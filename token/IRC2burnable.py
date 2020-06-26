import .IRC2
from iconservice import *

class IRC2Burnable(IRC2,IconScoreBase):

    @external
    def burn(self, _amount: int) -> None:
        # _burn is from IRC2
        _burn(msg.sender, _amount)

    @external
    def burnFrom(self, _account: Address, _amount: int) -> None:
        self._decreasedAllowance = allowance(_account, msg.sender - _amount )

        #these are from IRC2
        _approve(_account, msg.sender, self._decreasedAllowance)
        _burn(_account, _amount)
