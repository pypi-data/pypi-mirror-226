from inspect import getmembers
from typing import Any
from pytest import MonkeyPatch
import functools
import io
import os
import socket
from .pytest_sandbox import MockOsModule
import builtins
import math
from dataclasses import is_dataclass, fields
from typing import Tuple


class MockedModule:
    pass


class ProhibitedFunctionCall(Exception):
    pass


def fn_doesnt_exist(module_name: str, fn_name: str):
    def swapped_fn_call(*args, **kwargs):
        raise ProhibitedFunctionCall(
            f"{module_name}.{fn_name} is prohibited during testing"
        )

    return swapped_fn_call


def swap_function_calls(monkey_patch_context, module, mocked_module, attrs_to_keep):
    for member in getmembers(module):
        fn_name = member[0]  # type: ignore
        if fn_name in attrs_to_keep:
            continue
        if callable(member[1]):
            if hasattr(mocked_module, fn_name):
                monkey_patch_context.setattr(
                    module, fn_name, getattr(mocked_module, fn_name)
                )
            else:
                monkey_patch_context.setattr(
                    module, fn_name, fn_doesnt_exist(module.__name__, fn_name)
                )


def patch_system_modules(test_fn):
    @functools.wraps(test_fn)
    def wrapped(*args, **kwargs):
        with MonkeyPatch.context() as m:
            fh = MockOsModule()
            m.setattr(io, "open", fh.open)
            m.setattr(builtins, "open", fh.open)
            swap_function_calls(m, os, fh, {"path", "fspath"})
            swap_function_calls(m, socket, MockedModule(), {})
            return test_fn(*args, **kwargs)

    return wrapped


def equals(a: Any, b: Any) -> bool:
    return equals_with_message(a, b)[0]


def eq_msg(a: Any, b: Any) -> str:
    return equals_with_message(a, b)[1]


def equals_with_message(a: Any, b: Any) -> Tuple[bool, str]:
    if type(a) != type(b):
        return False, f"Types don't match: {type(a)} != {type(b)}"
    obj_typ = type(a)
    if obj_typ == dict:
        a_keys_set = set(a.keys())
        b_keys_set = set(b.keys())
        keys_equal, msg = equals_with_message(a_keys_set, b_keys_set)
        if not keys_equal:
            return False, f"Dictionary keys don't match {msg}"
        for key in a.keys():
            val_eq, msg = equals_with_message(a[key], b[key])
            if not val_eq:
                return False, f"Dictionary values don't match for key {key}:\n{msg}"
        return True, ""
    elif obj_typ == list:
        if len(a) != len(b):
            return False, f"Lists don't have the same length: {len(a)} != {len(b)}"
        for i in range(len(a)):
            val_eq, msg = equals_with_message(a[i], b[i])
            if not val_eq:
                return False, f"List values don't match for index {i}: {msg}"
        return True, ""
    elif obj_typ == tuple:
        if len(a) != len(b):
            return False, f"Tuples don't have the same length: {len(a)} != {len(b)}"
        for i in range(len(a)):
            val_eq, msg = equals_with_message(a[i], b[i])
            if not val_eq:
                return False, f"Tuple values don't match for index {i}: {msg}"
        return True, ""
    elif obj_typ == set:
        if len(a) != len(b):
            return False, f"Sets don't have the same length: {len(a)} != {len(b)}"

        num_items_not_in_b = 0
        msg = ""
        for a_item in a:
            for b_item in b:
                if a_item.__hash__() == b_item.__hash__():
                    val_eq, val_msg = equals_with_message(a_item, b_item)
                    if val_eq:
                        break
                    else:
                        return (
                            False,
                            f"Set values don't match: {a_item} from left set != {b_item} from right set\n {val_msg}",
                        )
                elif equals(a_item, b_item):
                    break
            else:
                num_items_not_in_b += 1
                msg += f"{a_item} from left set not in right set\n"
        if num_items_not_in_b > 0:
            return False, f"Left set != Right set:\n {msg}"
        else:
            return True, ""
    elif obj_typ == float:
        return math.isclose(a, b), f"{a} != {b}"
    elif is_dataclass(obj_typ):
        if a == b:
            return True, ""
        for field in fields(obj_typ):
            if field.compare:
                val_eq, msg = equals_with_message(
                    getattr(a, field.name), getattr(b, field.name)
                )
                if not val_eq:
                    return (
                        False,
                        f"Values don't match for `{obj_typ}.{field.name}`\n {msg}",
                    )
        return True, ""
    elif (
        hasattr(obj_typ, "__eq__")
        and hasattr(obj_typ.__eq__, "__objclass__")
        and obj_typ.__eq__.__objclass__ == object  # type: ignore
    ):
        for member in getmembers(a):
            if member[0].startswith("_") or callable(member[1]):
                continue
            if not hasattr(b, member[0]):
                return (
                    False,
                    f"Right object of type `{obj_typ}` doesn't have the attribute `{member[0]}`",
                )
            val_eq, msg = equals_with_message(member[1], getattr(b, member[0]))
            if not val_eq:
                return (
                    False,
                    f"Values don't match for `{obj_typ}.{member[0]}`\n {msg}",
                )
        return True, ""
    else:
        return a == b, f"{a} != {b}"
