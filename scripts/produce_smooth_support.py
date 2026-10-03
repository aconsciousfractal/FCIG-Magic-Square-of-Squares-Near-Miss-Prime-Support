#!/usr/bin/env python3
"""Rebuild a witness catalogue and triangle/array atlases using integers only.

A bounded producer is NOT a completeness proof. The independent verifier uses
an explicitly imported global cardinality (von Kaenel--Matschke, Theorem A).
No downloaded solution list and no external computer-algebra system is used.
"""
from __future__ import annotations
import argparse
from bisect import bisect_right
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, permutations
import json
from math import gcd, isqrt, lcm
from pathlib import Path
import time

PRIMES = (2, 3, 5, 7, 11, 13, 17, 19)
ROOT = Path(__file__).resolve().parents[1]


def smooth_numbers(bound: int) -> list[tuple[int, int]]:
    values = [(1, 0)]
    for i, p in enumerate(PRIMES):
        extra = []
        for n, mask in values:
            power = n * p
            while power <= bound:
                extra.append((power, mask | (1 << i)))
                power *= p
        values += extra
    return sorted(values)


def abc_witnesses(bound: int) -> list[list[int]]:
    smooth = smooth_numbers(bound)
    masks = dict(smooth)
    choices: dict[int, list[int]] = {}
    rows = []
    for c, mask in smooth:
        if mask not in choices:
            choices[mask] = [v for v, m in smooth if not (m & mask)]
        candidates = choices[mask]
        for a in candidates[:bisect_right(candidates, c // 2)]:
            b = c - a
            if b in masks and not (masks[b] & mask):
                rows.append([a, b, c])
    return sorted(rows)


def residual(n: int, primes: tuple[int, ...]) -> int:
    if n <= 0:
        return n
    for p in primes:
        while n % p == 0:
            n //= p
    return n


def split_area(area: int, primes: tuple[int, ...]) -> tuple[int, int]:
    n, h = 1, 1
    for p in primes:
        e = 0
        while area % p == 0:
            area //= p
            e += 1
        n *= p ** (e % 2)
        h *= p ** (e // 2)
    if area != 1:
        raise ValueError('Area has a prime outside the declared support')
    return n, h


def triangles_by_difference(rows: list[list[int]], primes: tuple[int, ...]) -> list[dict]:
    """Use the record k+(m-k)=m, then test m+k separately."""
    found = {}
    for a, b, m in rows:
        for k in set((a, b)):
            if (m + k) % 2 == 0 or residual(m + k, primes) != 1:
                continue
            legs = sorted((2*m*k, m*m-k*k))
            hyp = m*m+k*k
            area = m*k*(m-k)*(m+k)
            n, h = split_area(area, primes)
            sigma = Fraction(hyp*hyp, h*h)
            found[m, k] = dict(m=m, k=k, legs=legs, hyp=hyp, area=area,
                               kernel=n, h=h, sigma=[sigma.numerator, sigma.denominator])
    return [found[key] for key in sorted(found)]


def canonical_roots(roots: tuple[int, ...]) -> tuple[int, ...]:
    def rotate(v):
        return tuple(v[(2-c)*3+r] for r in range(3) for c in range(3))
    def reflect(v):
        return tuple(v[3*r+2-c] for r in range(3) for c in range(3))
    orbit = []
    for _ in range(4):
        orbit += [roots, reflect(roots)]
        roots = rotate(roots)
    return min(orbit)


def make_atlas(triangles: list[dict]) -> list[dict]:
    groups = defaultdict(list)
    for row in triangles:
        groups[row['kernel']].append(row)
    atlas = {}
    for n, group in groups.items():
        for triple in combinations(group, 3):
            L = lcm(*(t['h'] for t in triple))
            centres = [Fraction(*t['sigma'])*L*L for t in triple]
            if any(c.denominator != 1 for c in centres):
                raise ValueError('Nonintegral centre after clearing root denominators')
            d = 4*n*L*L
            for A, E, P in permutations(map(int, centres)):
                for D in (d, -d):
                    values = (A, P+D, E-D, P-D, E, A+D, E+D, A-D, P)
                    if min(values) <= 0 or len(set(values)) != 9:
                        continue
                    roots = tuple(isqrt(x) for x in values)
                    if any(r*r != x for r, x in zip(roots, values)):
                        raise ValueError('Nonsquare reconstructed entry')
                    g = gcd(*roots)
                    roots = canonical_roots(tuple(r//g for r in roots))
                    if d % (g*g):
                        raise ValueError('Primitive difference is not integral')
                    key = roots
                    value = {'roots': list(roots), 'd': d//(g*g), 'kernel': n,
                             'euclid': sorted([[t['m'], t['k']] for t in triple])}
                    if key in atlas and atlas[key] != value:
                        raise ValueError('Inconsistent duplicate array')
                    atlas[key] = value
    return [atlas[key] for key in sorted(atlas)]


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bound', type=int, default=10**10,
                    help='Witness-generation bound only; not asserted to be a global height bound')
    ap.add_argument('--out', type=Path, default=ROOT/'certificates/smooth_support')
    args = ap.parse_args()
    if args.bound < 2:
        ap.error('--bound must be at least 2')
    start = time.monotonic()
    rows = abc_witnesses(args.bound)
    args.out.mkdir(parents=True, exist_ok=True)
    write_json(args.out/'abc_S19.json', rows)
    counts = {}
    for cutoff in (7, 13, 19):
        primes = tuple(p for p in PRIMES if p <= cutoff)
        subset = [r for r in rows if all(residual(x, primes)==1 for x in r)]
        triangles = triangles_by_difference(subset, primes)
        atlas = make_atlas(triangles)
        write_json(args.out/f'triangles_S{cutoff}.json', triangles)
        write_json(args.out/f'atlas_9_7_S{cutoff}.json', atlas)
        counts[cutoff] = {'abc':len(subset), 'triangles':len(triangles), 'arrays':len(atlas)}
    print(json.dumps({'status':'GENERATED_WITNESSES_NOT_A_COMPLETENESS_PROOF',
                      'bound':args.bound,'counts':counts,
                      'elapsed_seconds':round(time.monotonic()-start,3)},indent=2))

if __name__ == '__main__':
    main()
