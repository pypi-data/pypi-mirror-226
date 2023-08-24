from _typeshed import Incomplete
from enum import Enum as Enum
from typing import Dict
from typing_extensions import TypeAlias

F: str
C: str
E: str
W: str
N: str
I: str
D: str
T: str
all_levels: Incomplete
MsgTuple: TypeAlias

class msg(BaseException):
    M411_sdk_version_deprecated__version: Incomplete
    M412_method_deprecated__method_replacement: Incomplete
    M511_field_not_found_on_get__key_type_item: Incomplete
    M512_field_not_found_on_set__key_type_item: Incomplete
    M513_method_removed__method_replacement: Incomplete
    M514_create_called_on_relation__field: Incomplete
    M515_create_called_on_value__property: Incomplete
    M516_create_called_without_a_list: Incomplete
    M517_create_called_on_type__type_container: Incomplete
    M518_list_not_found_on_append__key_type_item_item2: Incomplete
    M519_called_class_constructor: Incomplete
    M520_item_not_found_in_list__key_item_list: Incomplete
    M521_item_not_iterable__item: Incomplete
    M522_set_called_with_invalid_type__field_key_rtype_etype: Incomplete
    M523_mismatched_expected_and_received_arguments__rtype_etype: Incomplete
    M524_missing_property_value__listname_propname: Incomplete
    M525_appending_existing_items__list_items: Incomplete
    M526_legacy_error: Incomplete
    M527_unknown_datatype_from_server: Incomplete
    M711_unexpected_exception__exception: Incomplete
    M811_server_timeout__url: Incomplete
    M812_server_invalid_url__url: Incomplete
    M813_connection_error__url: Incomplete
    M814_invalid_handshake__url: Incomplete
    M815_oserr_connection_error__errno_url: Incomplete
    @staticmethod
    def TRACEBACK_REWRITTEN_BELOW_FOR_CLARITY(python_class: type | int, short_desc_message: str, long_desc_message: str) -> None: ...
    class TellDevException(BaseException):
        e_msg: Incomplete
        e_args: Incomplete
        def __init__(self, msg: MsgTuple, args: Dict[str, str]) -> None: ...
