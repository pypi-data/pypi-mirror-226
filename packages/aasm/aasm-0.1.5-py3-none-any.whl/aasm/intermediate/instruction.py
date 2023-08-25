from __future__ import annotations

from typing import TYPE_CHECKING
from typing import List as TypingList

if TYPE_CHECKING:
    from aasm.intermediate.argument import Argument


class Instruction:
    def print(self) -> None:
        raise NotImplementedError()


class Comparaison(Instruction):
    def __init__(self, left: Argument, right: Argument):
        self.left = left
        self.right = right

    def print(self) -> None:
        print("Comparaison")
        self.left.print()
        self.right.print()


class IfGreaterThan(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("IfGreaterThan")
        super().print()


class IfGreaterThanOrEqual(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("IfGreaterThanOrEqual")
        super().print()


class IfLessThan(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("IfLessThan")
        super().print()


class IfLessThanOrEqual(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("IfLessThanOrEqual")
        super().print()


class IfEqual(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("IfEqual")
        super().print()


class IfNotEqual(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("IfNotEqual")
        super().print()


class WhileGreaterThan(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("WhileGreaterThan")
        super().print()


class WhileGreaterThanOrEqual(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("WhileGreaterThanOrEqual")
        super().print()


class WhileLessThan(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("WhileLessThan")
        super().print()


class WhileLessThanOrEqual(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("WhileLessThanOrEqual")
        super().print()


class WhileEqual(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("WhileEqual")
        super().print()


class WhileNotEqual(Comparaison):
    def __init__(self, left: Argument, right: Argument):
        super().__init__(left=left, right=right)

    def print(self) -> None:
        print("WhileNotEqual")
        super().print()


class MathOperation(Instruction):
    def __init__(self, dst: Argument, num: Argument):
        self.dst = dst
        self.num = num

    def print(self) -> None:
        print("MathOperation")
        self.dst.print()
        self.num.print()


class Multiply(MathOperation):
    def __init__(self, dst: Argument, num: Argument):
        super().__init__(dst=dst, num=num)

    def print(self) -> None:
        print("Multiply")
        super().print()


class Divide(MathOperation):
    def __init__(self, dst: Argument, num: Argument):
        super().__init__(dst=dst, num=num)

    def print(self) -> None:
        print("Divide")
        super().print()


class Add(MathOperation):
    def __init__(self, dst: Argument, num: Argument):
        super().__init__(dst=dst, num=num)

    def print(self) -> None:
        print("Add")
        super().print()


class Subtract(MathOperation):
    def __init__(self, dst: Argument, num: Argument):
        super().__init__(dst=dst, num=num)

    def print(self) -> None:
        print("Subtract")
        super().print()


class ListElementAccess(Instruction):
    def __init__(self, list_: Argument, element: Argument):
        self.list_ = list_
        self.element = element

    def print(self) -> None:
        print("ListElementAccess")
        self.list_.print()
        self.element.print()


class AddElement(ListElementAccess):
    def __init__(self, list_: Argument, element: Argument):
        super().__init__(list_=list_, element=element)

    def print(self) -> None:
        print("AddElement")
        super().print()


class RemoveElement(ListElementAccess):
    def __init__(self, list_: Argument, element: Argument):
        super().__init__(list_=list_, element=element)

    def print(self) -> None:
        print("RemoveElement")
        super().print()


class IfInList(ListElementAccess):
    def __init__(self, list_: Argument, element: Argument):
        super().__init__(list_=list_, element=element)

    def print(self) -> None:
        print("IfInList")
        super().print()


class IfNotInList(ListElementAccess):
    def __init__(self, list_: Argument, element: Argument):
        super().__init__(list_=list_, element=element)

    def print(self) -> None:
        print("IfNotInList")
        super().print()


class RemoveNElements(Instruction):
    def __init__(self, list_: Argument, num: Argument):
        self.list_ = list_
        self.num = num

    def print(self) -> None:
        print("RemoveNElements")
        self.list_.print()
        self.num.print()


class Subset(Instruction):
    def __init__(self, dst_list: Argument, src_list: Argument, num: Argument):
        self.dst_list = dst_list
        self.src_list = src_list
        self.num = num

    def print(self) -> None:
        print("Subset")
        self.dst_list.print()
        self.src_list.print()
        self.num.print()


class Set(Instruction):
    def __init__(self, dst: Argument, value: Argument):
        self.dst = dst
        self.value = value

    def print(self) -> None:
        print("Set")
        self.dst.print()
        self.value.print()


class Clear(Instruction):
    def __init__(self, list_: Argument):
        self.list_ = list_

    def print(self) -> None:
        print("Clear")
        self.list_.print()


class Length(Instruction):
    def __init__(self, dst: Argument, list_: Argument):
        self.dst = dst
        self.list_ = list_

    def print(self) -> None:
        print("Length")
        self.dst.print()
        self.list_.print()


class Send(Instruction):
    def __init__(self, receivers: Argument):
        self.receivers = receivers

    def print(self) -> None:
        print("Send")
        self.receivers.print()


class Round(Instruction):
    def __init__(self, dst: Argument):
        self.dst = dst

    def print(self) -> None:
        print("Round")
        self.dst.print()


class UniformDist(Instruction):
    def __init__(self, dst: Argument, a: Argument, b: Argument):
        self.dst = dst
        self.a = a
        self.b = b

    def print(self) -> None:
        print("UniformDist")
        self.dst.print()
        self.a.print()
        self.b.print()


class NormalDist(Instruction):
    def __init__(self, dst: Argument, mean: Argument, std_dev: Argument):
        self.dst = dst
        self.mean = mean
        self.std_dev = std_dev

    def print(self) -> None:
        print("NormalDist")
        self.dst.print()
        self.mean.print()
        self.std_dev.print()


class ExpDist(Instruction):
    def __init__(self, dst: Argument, lambda_: Argument):
        self.dst = dst
        self.lambda_ = lambda_

    def print(self) -> None:
        print("ExpDist")
        self.dst.print()
        self.lambda_.print()


class ListRead(Instruction):
    def __init__(self, dst: Argument, list_: Argument, idx: Argument):
        self.dst = dst
        self.list_ = list_
        self.idx = idx

    def print(self) -> None:
        print("ListRead")
        self.dst.print()
        self.list_.print()
        self.idx.print()


class ListWrite(Instruction):
    def __init__(self, list_: Argument, idx: Argument, value: Argument):
        self.list_ = list_
        self.idx = idx
        self.value = value

    def print(self) -> None:
        print("ListWrite")
        self.list_.print()
        self.idx.print()
        self.value.print()


class TrigonometryOperation(Instruction):
    def __init__(self, dst: Argument, degree: Argument):
        self.dst = dst
        self.degree = degree

    def print(self) -> None:
        print("TrigonometryOperation")
        self.dst.print()
        self.degree.print()


class Sin(TrigonometryOperation):
    def __init__(self, dst: Argument, degree: Argument):
        super().__init__(dst=dst, degree=degree)

    def print(self) -> None:
        print("Sin")
        super().print()


class Cos(TrigonometryOperation):
    def __init__(self, dst: Argument, degree: Argument):
        super().__init__(dst=dst, degree=degree)

    def print(self) -> None:
        print("Cos")
        super().print()


class ExponentiationOperation(Instruction):
    def __init__(self, dst: Argument, base: Argument, num: Argument):
        self.dst = dst
        self.base = base
        self.num = num

    def print(self) -> None:
        print("ExponentiationOperation")
        self.dst.print()
        self.base.print()
        self.num.print()


class Logarithm(ExponentiationOperation):
    def __init__(self, dst: Argument, base: Argument, num: Argument):
        super().__init__(dst=dst, base=base, num=num)

    def print(self) -> None:
        print("Logarithm")
        super().print()


class Power(ExponentiationOperation):
    def __init__(self, dst: Argument, base: Argument, num: Argument):
        super().__init__(dst=dst, base=base, num=num)

    def print(self) -> None:
        print("Power")
        super().print()


class Modulo(Instruction):
    def __init__(self, dst: Argument, dividend: Argument, divisor: Argument):
        self.dst = dst
        self.dividend = dividend
        self.divisor = divisor

    def print(self) -> None:
        print("Modulo")
        self.dst.print()
        self.dividend.print()
        self.divisor.print()


class ModuleInstruction(Instruction):
    def __init__(
        self,
        args: TypingList[Argument],
        op_code: str = "",
        module: str = "",
        is_block=False,
        assignment: Argument | None = None,
    ):
        self.args: TypingList[Argument] = args
        self.op_code: str = op_code
        self.module: str = module
        self.is_block: bool = is_block
        self.assignment: Argument | None = assignment

    def print(self) -> None:
        print(f"{self.module}::{self.op_code}")
        for arg in self.args:
            arg.print()


class Logs(Instruction):
    def __init__(self, args: TypingList[Argument]):
        self.args = args

    def print(self) -> None:
        print("Logs")
        for arg in self.args:
            arg.print()


class LogsDebug(Logs):
    def __init__(self, args: TypingList[Argument]):
        super().__init__(args=args)

    def print(self) -> None:
        print("LogsDebug")
        super().print()


class LogsInfo(Logs):
    def __init__(self, args: TypingList[Argument]):
        super().__init__(args=args)

    def print(self) -> None:
        print("LogsInfo")
        super().print()


class LogsWarning(Logs):
    def __init__(self, args: TypingList[Argument]):
        super().__init__(args=args)

    def print(self) -> None:
        print("LogsWarning")
        super().print()


class LogsError(Logs):
    def __init__(self, args: TypingList[Argument]):
        super().__init__(args=args)

    def print(self) -> None:
        print("LogsError")
        super().print()


class LogsCritical(Logs):
    def __init__(self, args: TypingList[Argument]):
        super().__init__(args=args)

    def print(self) -> None:
        print("LogsCritical")
        super().print()
