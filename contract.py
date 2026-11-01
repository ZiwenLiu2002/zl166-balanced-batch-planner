"""Typed inputs and outputs for the balanced batch planner."""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Tool(Enum):
    EVALUATE_PARTITION = "evaluate_partition"
    SOLVE_PARTITION = "solve_partition"


class Task(Enum):
    BALANCE_BATCHES = "balance-batches"


class Status(Enum):
    SOLVED = "solved"
    INFEASIBLE = "infeasible"


@dataclass
class Item(Output):
    id: Annotated[str, "A unique non-empty item identifier"]
    weight: Annotated[int, "The item's non-negative integer weight"]


@dataclass
class BalanceInput(Output):
    items: Annotated[list[Item], "Between 1 and 10 uniquely named items"]
    batch_count: Annotated[int, "Number of non-empty batches, between 1 and 4"]


@dataclass
class EvaluateInput(Output):
    items: Annotated[list[Item], "The items to partition"]
    batch_count: Annotated[int, "The required number of non-empty batches"]
    batches: Annotated[list[list[str]], "A proposed partition, as lists of item identifiers"]


@dataclass
class BalanceOutput(Output):
    status: Annotated[Status, "Whether a valid partition exists"]
    batches: Annotated[list[list[str]], "Canonical batches: sorted identifiers, then sorted batches"]
    loads: Annotated[list[int], "Each canonical batch's total weight"]
    max_load: Annotated[int, "The greatest batch load, or zero when infeasible"]


TOOLS = {
    Tool.EVALUATE_PARTITION: (EvaluateInput, BalanceOutput),
    Tool.SOLVE_PARTITION: (BalanceInput, BalanceOutput),
}
TASKS = {Task.BALANCE_BATCHES: (BalanceInput, BalanceOutput)}
