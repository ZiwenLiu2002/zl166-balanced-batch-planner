from contract import Task, Tool

from .checks import input_problem, optimal_key, output_problem, result


def verify_input(tool, value):
    problem = input_problem(value)
    if Tool(tool) == Tool.EVALUATE_PARTITION and not value.batches:
        problem = problem or "a candidate must contain batches"
    return result(problem is None, problem or "input is valid")


def verify_output(tool, input_value, output_value, workspace):
    if Tool(tool) == Tool.EVALUATE_PARTITION:
        problem = output_problem(input_value, output_value)
    else:
        problem = output_problem(input_value, output_value)
        if problem is None:
            expected = optimal_key(input_value)
            actual = (output_value.max_load, tuple(tuple(batch) for batch in output_value.batches))
            if actual != expected:
                problem = "solver output is not the canonical optimum"
    return result(problem is None, problem or "output is valid")


def verify_task(task, arguments, output, reference, workspace):
    if Task(task) != Task.BALANCE_BATCHES:
        return result(False, "unknown task")
    problem = input_problem(arguments) or output_problem(arguments, output)
    if problem is None:
        expected = optimal_key(arguments)
        actual = (output.max_load, tuple(tuple(batch) for batch in output.batches))
        if actual != expected:
            problem = "partition is not the canonical optimum"
    if problem is None and reference is not None and output.max_load != reference.max_load:
        problem = "partition disagrees with the hidden optimum"
    return result(problem is None, problem or "partition is optimal")
