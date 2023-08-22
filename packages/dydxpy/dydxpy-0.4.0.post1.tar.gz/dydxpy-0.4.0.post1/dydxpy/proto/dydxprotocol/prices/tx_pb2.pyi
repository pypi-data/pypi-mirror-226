from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgUpdateMarketPrices(_message.Message):
    __slots__ = ["market_price_updates"]
    class MarketPrice(_message.Message):
        __slots__ = ["market_id", "price"]
        MARKET_ID_FIELD_NUMBER: _ClassVar[int]
        PRICE_FIELD_NUMBER: _ClassVar[int]
        market_id: int
        price: int
        def __init__(self, market_id: _Optional[int] = ..., price: _Optional[int] = ...) -> None: ...
    MARKET_PRICE_UPDATES_FIELD_NUMBER: _ClassVar[int]
    market_price_updates: _containers.RepeatedCompositeFieldContainer[MsgUpdateMarketPrices.MarketPrice]
    def __init__(self, market_price_updates: _Optional[_Iterable[_Union[MsgUpdateMarketPrices.MarketPrice, _Mapping]]] = ...) -> None: ...

class MsgUpdateMarketPricesResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
