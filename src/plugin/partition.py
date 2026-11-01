from contract import BalanceInput, BalanceOutput, EvaluateInput, Status


def _problem(items, batch_count):
    ids = [item.id for item in items]
    if not 1 <= len(items) <= 10:
        return "items must contain between 1 and 10 entries"
    if len(set(ids)) != len(ids) or any(not name.strip() for name in ids):
        return "item ids must be unique and non-empty"
    if any(item.weight < 0 or item.weight > 1000 for item in items):
        return "weights must be between 0 and 1000"
    if not 1 <= batch_count <= min(4, len(items)):
        return "batch_count must be between 1 and min(4, number of items)"
    return None


def _canonical(batches):
    return sorted((sorted(batch) for batch in batches), key=lambda batch: tuple(batch))


def _output(items, batch_count, batches):
    if _problem(items, batch_count):
        return BalanceOutput(status=Status.INFEASIBLE, batches=[], loads=[], max_load=0)
    expected = {item.id for item in items}
    flat = [name for batch in batches for name in batch]
    if len(batches) != batch_count or any(not batch for batch in batches) or len(flat) != len(set(flat)) or set(flat) != expected:
        return BalanceOutput(status=Status.INFEASIBLE, batches=[], loads=[], max_load=0)
    canonical = _canonical(batches)
    weights = {item.id: item.weight for item in items}
    loads = [sum(weights[name] for name in batch) for batch in canonical]
    return BalanceOutput(status=Status.SOLVED, batches=canonical, loads=loads, max_load=max(loads))


def evaluate_partition(value: EvaluateInput, workspace):
    return _output(value.items, value.batch_count, value.batches)


def solve_partition(value: BalanceInput, workspace):
    if _problem(value.items, value.batch_count):
        return BalanceOutput(status=Status.INFEASIBLE, batches=[], loads=[], max_load=0)
    names = sorted(item.id for item in value.items)
    best = None

    def visit(index, batches):
        nonlocal best
        if index == len(names):
            if len(batches) == value.batch_count:
                candidate = _output(value.items, value.batch_count, batches)
                key = (candidate.max_load, tuple(tuple(batch) for batch in candidate.batches))
                if best is None or key < best[0]:
                    best = (key, candidate)
            return
        name = names[index]
        for position in range(len(batches)):
            batches[position].append(name)
            visit(index + 1, batches)
            batches[position].pop()
        if len(batches) < value.batch_count:
            batches.append([name])
            visit(index + 1, batches)
            batches.pop()

    visit(0, [])
    return best[1]
