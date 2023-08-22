from gogoproto import gogo_pb2 as _gogo_pb2
from dydxprotocol.clob import order_pb2 as _order_pb2
from dydxprotocol.clob import order_removals_pb2 as _order_removals_pb2
from dydxprotocol.clob import matches_pb2 as _matches_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgProposedOperations(_message.Message):
    __slots__ = ["operations_queue"]
    OPERATIONS_QUEUE_FIELD_NUMBER: _ClassVar[int]
    operations_queue: _containers.RepeatedCompositeFieldContainer[OperationRaw]
    def __init__(self, operations_queue: _Optional[_Iterable[_Union[OperationRaw, _Mapping]]] = ...) -> None: ...

class MsgProposedOperationsResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgPlaceOrder(_message.Message):
    __slots__ = ["order"]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    order: _order_pb2.Order
    def __init__(self, order: _Optional[_Union[_order_pb2.Order, _Mapping]] = ...) -> None: ...

class MsgPlaceOrderResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MsgCancelOrder(_message.Message):
    __slots__ = ["order_id", "good_til_block", "good_til_block_time"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    GOOD_TIL_BLOCK_FIELD_NUMBER: _ClassVar[int]
    GOOD_TIL_BLOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    order_id: _order_pb2.OrderId
    good_til_block: int
    good_til_block_time: int
    def __init__(self, order_id: _Optional[_Union[_order_pb2.OrderId, _Mapping]] = ..., good_til_block: _Optional[int] = ..., good_til_block_time: _Optional[int] = ...) -> None: ...

class MsgCancelOrderResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class OperationRaw(_message.Message):
    __slots__ = ["match", "short_term_order_placement", "order_removal"]
    MATCH_FIELD_NUMBER: _ClassVar[int]
    SHORT_TERM_ORDER_PLACEMENT_FIELD_NUMBER: _ClassVar[int]
    ORDER_REMOVAL_FIELD_NUMBER: _ClassVar[int]
    match: _matches_pb2.ClobMatch
    short_term_order_placement: bytes
    order_removal: _order_removals_pb2.OrderRemoval
    def __init__(self, match: _Optional[_Union[_matches_pb2.ClobMatch, _Mapping]] = ..., short_term_order_placement: _Optional[bytes] = ..., order_removal: _Optional[_Union[_order_removals_pb2.OrderRemoval, _Mapping]] = ...) -> None: ...
