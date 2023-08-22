from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FundingPremium(_message.Message):
    __slots__ = ["perpetual_id", "premium_ppm"]
    PERPETUAL_ID_FIELD_NUMBER: _ClassVar[int]
    PREMIUM_PPM_FIELD_NUMBER: _ClassVar[int]
    perpetual_id: int
    premium_ppm: int
    def __init__(self, perpetual_id: _Optional[int] = ..., premium_ppm: _Optional[int] = ...) -> None: ...

class MsgAddPremiumVotes(_message.Message):
    __slots__ = ["votes"]
    VOTES_FIELD_NUMBER: _ClassVar[int]
    votes: _containers.RepeatedCompositeFieldContainer[FundingPremium]
    def __init__(self, votes: _Optional[_Iterable[_Union[FundingPremium, _Mapping]]] = ...) -> None: ...

class MsgAddPremiumVotesResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
