from pathlib import Path

from slimconfig import build_output

import verifier
from contract import TASKS, TOOLS, Task, Tool


def task_verdict(arguments, output):
    given, made = TASKS[Task.BALANCE_BATCHES]
    return verifier.verify_task(
        Task.BALANCE_BATCHES.value,
        build_output(arguments, given),
        build_output(output, made),
        None,
        Path("."),
    )


def test_accepts_canonical_optimum():
    arguments = {"items": [{"id": "a", "weight": 5}, {"id": "b", "weight": 4}, {"id": "c", "weight": 3}], "batch_count": 2}
    output = {"status": "solved", "batches": [["a"], ["b", "c"]], "loads": [5, 7], "max_load": 7}
    assert task_verdict(arguments, output)["valid"] is True


def test_rejects_missing_duplicate_and_forged_loads():
    arguments = {"items": [{"id": "a", "weight": 5}, {"id": "b", "weight": 4}, {"id": "c", "weight": 3}], "batch_count": 2}
    base = {"status": "solved", "batches": [["a"], ["b", "c"]], "loads": [5, 7], "max_load": 7}
    assert task_verdict(arguments, base | {"batches": [["a"], ["b"]]})["valid"] is False
    assert task_verdict(arguments, base | {"batches": [["a"], ["b", "b", "c"]]})["valid"] is False
    assert task_verdict(arguments, base | {"loads": [5, 6]})["valid"] is False
    assert task_verdict(arguments, base | {"max_load": 1})["valid"] is False


def test_rejects_valid_but_nonoptimal_partition():
    arguments = {"items": [{"id": "a", "weight": 8}, {"id": "b", "weight": 7}, {"id": "c", "weight": 6}, {"id": "d", "weight": 5}], "batch_count": 2}
    output = {"status": "solved", "batches": [["a", "b"], ["c", "d"]], "loads": [15, 11], "max_load": 15}
    assert task_verdict(arguments, output)["valid"] is False


def test_input_boundaries():
    cls = TOOLS[Tool.SOLVE_PARTITION][0]
    one = build_output({"items": [{"id": "x", "weight": 0}], "batch_count": 1}, cls)
    assert verifier.verify_input("solve_partition", one)["valid"] is True
    duplicate = build_output({"items": [{"id": "x", "weight": 1}, {"id": "x", "weight": 2}], "batch_count": 1}, cls)
    assert verifier.verify_input("solve_partition", duplicate)["valid"] is False
    too_many = build_output({"items": [{"id": "x", "weight": 1}], "batch_count": 2}, cls)
    assert verifier.verify_input("solve_partition", too_many)["valid"] is False
