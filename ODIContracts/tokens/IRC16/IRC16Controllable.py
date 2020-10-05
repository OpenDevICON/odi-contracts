from iconservice import *
from .IRC16 import *

class IRC16Controllable(IRC16):

    @eventlog(indexed=1)
    def Paused(self, status:bool):
        pass

    @external(readonly=True)
    def isControllable(self) -> bool:
        return self._controllable.get()

    @external
    def addController(self, _account: Address):
        super()._addController(_account)

    @external
    def removeController(self, _account: Address):
        super()._removeController(_account)

    @external
    def controllerTransferByPartition(self, _partition: str, _from: Address, _to: Address, _amount: int, _data: bytes = None) -> None:
        if self.msg.sender not in self._controllers:
            revert("Only controllers have access to this method.")
        super()._transferByPartition(_partition, self.msg.sender, _from, _to, _amount, _data)