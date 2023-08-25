import keyword
from decimal import Decimal
from typing import List

from aasm.utils.iteration import zip_consecutive_pairs


def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_int(value: str) -> bool:
    if value == "":
        return False
    return value.isdigit() or (value[0] == "-" and value[1:].isdigit())


def is_connection(value: str) -> bool:
    return isinstance(value, str) and value.startswith('"') and value.endswith('"')


def is_valid_enum_list(enums: List[str]) -> bool:
    if len(enums) == 0 or len(enums) % 2:
        return False
    total_sum = Decimal(0.0)
    for enum_pair in zip_consecutive_pairs(enums):
        if not is_float(enum_pair[1]) or float(enum_pair[1]) < 0.0:
            return False
        total_sum += Decimal(float(enum_pair[1]))
    if total_sum < 99.0 or total_sum > 101.0:
        return False
    return True


def is_valid_name(name: str) -> bool:
    return (
        len(name) != 0
        and not name[0].isdigit()
        and (name.isalnum() or "_" in name)
        and name.lower() not in get_invalid_names()
    )


def get_invalid_names() -> List[str]:
    invalid_names = [
        "send",
        "rcv",
        "len",
        "round",
        "list",
        "filter",
        "self",
        "jid",
        "datetime",
        "random",
        "numpy",
        "json",
        "spade",
        "copy",
        "uuid",
        "inspect",
        "get_json_from_spade_message",
        "get_spade_message",
        "logger",
        "any",
        "limit_number",
        "int",
        "BackupBehaviour",
        "backup_url",
        "backup_period",
        "backup_delay",
        "setup",
        "str",
        "float",
    ]
    invalid_names.extend(keyword.kwlist)
    return invalid_names


def print_invalid_names() -> str:
    return ", ".join(get_invalid_names())


def get_valid_logs_levels() -> List[str]:
    return ["debug", "info", "warning", "error", "critical"]


def print_valid_logs_levels() -> str:
    return ", ".join(get_valid_logs_levels())
