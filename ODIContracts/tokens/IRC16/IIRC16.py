from iconservice import *

TAG = 'SampleToken'


# An interface of ICON Token Standard, IRC-16
class TokenStandard(ABC):
    '''
    Normal token methods
    '''
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def symbol(self) -> str:
        pass

    @abstractmethod
    def decimals(self) -> int:
        pass

    @abstractmethod
    def totalSupply(self) -> int:
        pass

    @abstractmethod
    def balanceOf(self, _owner: Address) -> int:
        pass

    @abstractmethod
    def transfer(self, _to: Address, _value: int, _data: bytes = None):
        pass

    ''' 
    Partitions
    '''
    @abstractmethod
    def balanceOfByPartition(self, _partition: str, _owner: Address) -> int:
        pass

    @abstractmethod
    def partitionsOf(self, _owner: Address) -> dict:
        pass

    @abstractmethod
    def getDocument(self, _name: str) -> dict:
        pass

    @abstractmethod
    def setDocument(self, _name: str, _uri: str, _document_hash: str) -> None:
        pass

    @abstractmethod
    def transferByPartition(self, _partition: str, _to: Address, _amount: int, _data: bytes = None) -> None:
        pass

    @abstractmethod
    def operatorTransferByPartition(self, _partition: str, _from: Address, _to: Address, _amount: int, _data: bytes = None) -> None:
        pass

    @abstractmethod
    def authorizeOperator(self, _operator: Address) -> None:
        pass

    @abstractmethod
    def revokeOperator(self, _operator: Address) -> None:
        pass

    @abstractmethod
    def authorizeOperatorForPartition(self, _partition: str, _operator: Address) -> None:
        pass

    @abstractmethod
    def revokeOperatorForPartition(self, _partition: str, _operator: Address) -> None:
        pass