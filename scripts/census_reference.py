#!/usr/bin/env python3
"""Independent centre/difference census for Appendix A.

This is the first of the two independent census implementations shipped here.
It scans arithmetic-progression centres and differences.  The census family in
``verify.py`` is intentionally separate: it constructs full progressions
from root triples and partial progressions from root pairs.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


Grid = tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]


def is_square(value: int) -> bool:
    return value >= 0 and math.isqrt(value) ** 2 == value


def rotate(grid: Grid) -> Grid:
    return tuple(
        tuple(grid[2 - col][row] for col in range(3)) for row in range(3)
    )  # type: ignore[return-value]


def reflect(grid: Grid) -> Grid:
    return tuple(tuple(reversed(row)) for row in grid)  # type: ignore[return-value]


def canonical_d4(grid: Grid) -> Grid:
    forms: set[Grid] = set()
    current = grid
    for _ in range(4):
        forms.add(current)
        forms.add(reflect(current))
        current = rotate(current)
    return min(forms)


def line_sums(grid: Grid) -> tuple[int, ...]:
    rows = tuple(sum(row) for row in grid)
    cols = tuple(sum(grid[row][col] for row in range(3)) for col in range(3))
    diags = (
        grid[0][0] + grid[1][1] + grid[2][2],
        grid[0][2] + grid[1][1] + grid[2][0],
    )
    return rows + cols + diags


def universal_grid(a: int, p: int, e: int, delta: int) -> Grid:
    return (
        (a, p + delta, e - delta),
        (p - delta, e, a + delta),
        (e + delta, a - delta, p),
    )


def valid_grid(grid: Grid, root_bound: int) -> bool:
    entries = [value for row in grid for value in row]
    if min(entries) <= 0 or len(set(entries)) != 9:
        return False
    square_entries = [value for value in entries if is_square(value)]
    if len(square_entries) != 8:
        return False
    if max(math.isqrt(value) for value in square_entries) > root_bound:
        return False
    return sorted(Counter(line_sums(grid)).values()) == [1, 7]


def enumerate_classes(root_bound: int) -> set[Grid]:
    maximum = root_bound * root_bound
    squares = {root * root for root in range(1, root_bound + 1)}
    full: dict[int, set[tuple[int, int, int]]] = defaultdict(set)
    partial: dict[int, set[tuple[int, int, int]]] = defaultdict(set)

    for delta in range(1, maximum):
        for centre in range(delta + 1, maximum + 1):
            triple = (centre - delta, centre, centre + delta)
            count = sum(value in squares for value in triple)
            if count == 3:
                full[delta].add(triple)
            elif count == 2:
                partial[delta].add(triple)

    classes: set[Grid] = set()
    for delta in sorted(set(full) & set(partial)):
        for first, second in itertools.combinations(sorted(full[delta]), 2):
            for third in sorted(partial[delta]):
                if len(set(first + second + third)) != 9:
                    continue
                for ap_a, ap_p, ap_e in itertools.permutations(
                    (first, second, third)
                ):
                    grid = universal_grid(ap_a[1], ap_p[1], ap_e[1], delta)
                    if valid_grid(grid, root_bound):
                        classes.add(canonical_d4(grid))
    return classes


def main() -> int:
    classes46 = enumerate_classes(46)
    classes47 = enumerate_classes(47)
    centre_nonsquare = [grid for grid in classes47 if not is_square(grid[1][1])]
    if classes46 or len(classes47) != 9 or len(centre_nonsquare) != 2:
        raise RuntimeError("reference census disagrees with the frozen statement")
    representatives = [
        [list(row) for row in grid] for grid in sorted(classes47)
    ]
    frozen = json.loads(
        (Path(__file__).resolve().parent.parent
         / "certificates" / "expected_verification.json").read_text(
             encoding="utf-8"
         )
    )["families"]["family9_height_census"]["canonical_representatives"]
    if representatives != frozen:
        raise RuntimeError("reference census disagrees with verifier output")
    payload = {
        "algorithm": "integer_progression_centres_and_differences",
        "agreement_with_verifier_frozen_output": True,
        "height_46_d4_classes": len(classes46),
        "height_47_d4_classes": len(classes47),
        "height_47_centre_nonsquare_classes": len(centre_nonsquare),
        "height_47_canonical_representatives": representatives,
        "status": "PASS",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
