from contract import Status


def result(valid, message, **details):
    return {"valid": valid, "score": float(valid), "message": message, "details": details}


def input_problem(value):
    ids = [item.id for item in value.items]
    if not 1 <= len(value.items) <= 10:
        return "items must contain between 1 and 10 entries"
    if len(set(ids)) != len(ids) or any(not name.strip() for name in ids):
        return "item ids must be unique and non-empty"
    if any(item.weight < 0 or item.weight > 1000 for item in value.items):
        return "weights must be between 0 and 1000"
    if not 1 <= value.batch_count <= min(4, len(value.items)):
        return "invalid batch_count"
    return None


def output_problem(arguments, output):
    if output.status != Status.SOLVED:
        return "a valid problem must have solved status"
    if len(output.batches) != arguments.batch_count or any(not batch for batch in output.batches):
        return "wrong number of non-empty batches"
    canonical = sorted((sorted(batch) for batch in output.batches), key=lambda batch: tuple(batch))
    if output.batches != canonical:
        return "batches are not canonical"
    expected = [item.id for item in arguments.items]
    flat = [name for batch in output.batches for name in batch]
    if len(flat) != len(set(flat)) or sorted(flat) != sorted(expected):
        return "items are missing, duplicated, or unknown"
    weights = {item.id: item.weight for item in arguments.items}
    loads = [sum(weights[name] for name in batch) for batch in output.batches]
    if output.loads != loads:
        return "loads do not match the batches"
    if output.max_load != max(loads):
        return "max_load does not match the loads"
    return None


def optimal_key(arguments):
    names = sorted(item.id for item in arguments.items)
    weights = {item.id: item.weight for item in arguments.items}
    best = None

    def visit(index, batches):
        nonlocal best
        if index == len(names):
            if len(batches) == arguments.batch_count:
                canonical = sorted((sorted(batch) for batch in batches), key=lambda batch: tuple(batch))
                loads = [sum(weights[name] for name in batch) for batch in canonical]
                key = (max(loads), tuple(tuple(batch) for batch in canonical))
                if best is None or key < best:
                    best = key
            return
        name = names[index]
        for position in range(len(batches)):
            batches[position].append(name)
            visit(index + 1, batches)
            batches[position].pop()
        if len(batches) < arguments.batch_count:
            batches.append([name])
            visit(index + 1, batches)
            batches.pop()

    visit(0, [])
    return best
