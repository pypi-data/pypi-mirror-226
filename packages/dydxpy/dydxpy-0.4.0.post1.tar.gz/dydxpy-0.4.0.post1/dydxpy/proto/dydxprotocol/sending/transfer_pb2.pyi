from cosmos_proto import cosmos_pb2 as _cosmos_pb2
from cosmos.msg.v1 import msg_pb2 as _msg_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from dydxprotocol.subaccounts import subaccount_pb2 as _subaccount_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Transfer(_message.Message):
    __slots__ = ["sender", "recipient", "asset_id", "amount"]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    sender: _subaccount_pb2.SubaccountId
    recipient: _subaccount_pb2.SubaccountId
    asset_id: int
    amount: int
    def __init__(self, sender: _Optional[_Union[_subaccount_pb2.SubaccountId, _Mapping]] = ..., recipient: _Optional[_Union[_subaccount_pb2.SubaccountId, _Mapping]] = ..., asset_id: _Optional[int] = ..., amount: _Optional[int] = ...) -> None: ...

class MsgDepositToSubaccount(_message.Message):
    __slots__ = ["sender", "recipient", "asset_id", "quantums"]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTUMS_FIELD_NUMBER: _ClassVar[int]
    sender: str
    recipient: _subaccount_pb2.SubaccountId
    asset_id: int
    quantums: int
    def __init__(self, sender: _Optional[str] = ..., recipient: _Optional[_Union[_subaccount_pb2.SubaccountId, _Mapping]] = ..., asset_id: _Optional[int] = ..., quantums: _Optional[int] = ...) -> None: ...

class MsgWithdrawFromSubaccount(_message.Message):
    __slots__ = ["sender", "recipient", "asset_id", "quantums"]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    ASSET_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTUMS_FIELD_NUMBER: _ClassVar[int]
    sender: _subaccount_pb2.SubaccountId
    recipient: str
    asset_id: int
    quantums: int
    def __init__(self, sender: _Optional[_Union[_subaccount_pb2.SubaccountId, _Mapping]] = ..., recipient: _Optional[str] = ..., asset_id: _Optional[int] = ..., quantums: _Optional[int] = ...) -> None: ...
