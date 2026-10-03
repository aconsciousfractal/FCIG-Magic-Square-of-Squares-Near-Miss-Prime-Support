#!/usr/bin/env python3
"""Independent exact checker for the smooth-difference result.

Trust boundary: the global ABC cardinality is imported from the primary
von Kaenel--Matschke Theorem A; this program does NOT re-prove that theorem.
Everything downstream is reconstructed with Python integer/Fraction arithmetic.
The producer is neither imported nor executed by this checker. No asserts are
used, so checks remain active under python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations
import json
from math import gcd, isqrt, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19)
# Imported theorem inputs, not numbers inferred from the witness files:
IMPORTED_COUNTS = {7: 63, 13: 545, 19: 3649}


class VerificationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def factor_over(n: int, primes: tuple[int, ...]) -> tuple[list[int], int]:
    require(type(n) is int and n > 0, 'DOMAIN: expected positive integer (not bool)')
    valuations = []
    for p in primes:
        e = 0
        while n % p == 0:
            n //= p
            e += 1
        valuations.append(e)
    return valuations, n


def is_supported(n: int, primes: tuple[int, ...]) -> bool:
    return factor_over(n, primes)[1] == 1


def validate_abc(data: object, cutoff: int) -> tuple[tuple[int, int, int], ...]:
    require(cutoff in IMPORTED_COUNTS, 'IMPORT: unsupported prime cutoff')
    primes = tuple(p for p in PRIMES if p <= cutoff)
    require(type(data) is list, 'SHAPE: ABC certificate must be a list')
    seen = set()
    normalized = []
    for index, row in enumerate(data):
        require(type(row) is list and len(row) == 3, f'SHAPE: ABC row {index}')
        require(all(type(x) is int and x > 0 for x in row), f'DOMAIN: ABC row {index}')
        a, b, c = row
        require(a <= b < c and a+b == c, f'ADDITION: ABC row {index}')
        require(gcd(a, b) == 1, f'PRIMITIVITY: ABC row {index}')
        require(all(is_supported(x, primes) for x in row), f'SUPPORT: ABC row {index}')
        tup = (a, b, c)
        require(tup not in seen, f'DUPLICATE: ABC row {index}')
        seen.add(tup)
        normalized.append(tup)
    require(len(seen) == IMPORTED_COUNTS[cutoff],
            f'COUNT: found {len(seen)}, imported total {IMPORTED_COUNTS[cutoff]}')
    require(normalized == sorted(normalized), 'ORDER: ABC certificate is not sorted')
    return tuple(normalized)


def triangles_by_join(rows: tuple[tuple[int,int,int], ...], cutoff: int) -> list[dict]:
    """Independent direction: start from k+m=m+k and require k+(m-k)=m.

    Opposite parity means the third coordinate m+k is odd. Both additive
    records must occur in the fully checked ABC set. This differs from the
    producer's iteration over difference records plus a smoothness filter.
    """
    primes = tuple(p for p in PRIMES if p <= cutoff)
    registry = set(rows)
    found = []
    for k, m, c in rows:
        if k == m or c % 2 == 0:
            continue
        first = (min(k, m-k), max(k, m-k), m)
        if first not in registry:
            continue
        odd_leg, even_leg, hyp = m*m-k*k, 2*m*k, m*m+k*k
        require(gcd(odd_leg, even_leg) == 1, 'TRIANGLE: nonprimitive legs')
        require(odd_leg*odd_leg+even_leg*even_leg == hyp*hyp, 'TRIANGLE: Pythagorean identity')
        area = odd_leg*even_leg//2
        valuations, remainder = factor_over(area, primes)
        require(remainder == 1, 'TRIANGLE: area support')
        kernel = 1
        h = 1
        for p, e in zip(primes, valuations):
            if e & 1:
                kernel *= p
            h *= p**(e//2)
        require(kernel*h*h == area, 'TRIANGLE: squareclass split')
        sigma = Q(hyp, h)**2
        require(sigma > 4*kernel, 'TRIANGLE: nonpositive normalized root')
        found.append(dict(m=m,k=k,legs=sorted([odd_leg,even_leg]),hyp=hyp,
                          area=area,kernel=kernel,h=h,
                          sigma=[sigma.numerator,sigma.denominator]))
    found.sort(key=lambda r:(r['m'],r['k']))
    require(len({(r['m'],r['k']) for r in found}) == len(found), 'TRIANGLE: duplicate parameters')
    return found


def midpoint_hits(centres: list[Q]) -> tuple[int, list[list[Q]]]:
    registry = set(centres)
    require(len(registry) == len(centres), 'CENTRES: duplicate')
    tests = 0
    hits = []
    for low, high in combinations(sorted(registry), 2):
        tests += 1
        middle = (low+high)/2
        if middle in registry:
            hits.append([low, middle, high])
    return tests, hits


def rational_square_root(q: Q) -> Q:
    require(q > 0, 'ROOT: nonpositive entry')
    u, v = isqrt(q.numerator), isqrt(q.denominator)
    require(u*u == q.numerator and v*v == q.denominator, 'ROOT: entry is not a rational square')
    return Q(u, v)


def canonical_by_coordinates(roots: tuple[int, ...]) -> tuple[int, ...]:
    """Eight coordinate maps, without the producer's rotation recursion."""
    images = []
    for swap in (False, True):
        for sx in (-1, 1):
            for sy in (-1, 1):
                image = [0]*9
                for row in range(3):
                    for col in range(3):
                        x, y = row-1, col-1
                        if swap:
                            x, y = y, x
                        rr, cc = sx*x+1, sy*y+1
                        image[3*rr+cc] = roots[3*row+col]
                images.append(tuple(image))
    require(len(set(images)) == 8, 'D4: expected free action for nine distinct entries')
    return min(images)


def line_data(roots: tuple[int, ...]) -> tuple[int, int, int]:
    squares = [r*r for r in roots]
    sums = ([sum(squares[3*r:3*r+3]) for r in range(3)]
            + [sum(squares[c::3]) for c in range(3)]
            + [squares[0]+squares[4]+squares[8], squares[2]+squares[4]+squares[6]])
    counts = Counter(sums)
    require(sorted(counts.values()) == [1,7], f'LINES: not a (9,7) array: {sums}')
    common = next(s for s, k in counts.items() if k == 7)
    failed = next(s for s, k in counts.items() if k == 1)
    return common, failed, common-failed


def reconstruct_atlas(triangles: list[dict], cutoff: int) -> tuple[list[dict], dict]:
    primes = tuple(p for p in PRIMES if p <= cutoff)
    groups = defaultdict(list)
    for row in triangles:
        groups[row['kernel']].append(row)
    tests = 0
    for n, group in groups.items():
        pair_count, hits = midpoint_hits([Q(*r['sigma']) for r in group])
        tests += pair_count
        require(not hits, f'MAGIC_INTERACTION_FOUND: kernel={n}, centres={hits}')
    atlas = {}
    triple_count = 0
    rejected_triples = 0
    minimum = None
    minima = set()
    decorated = {}
    for n, group in sorted(groups.items()):
        group.sort(key=lambda r:Q(*r['sigma']))
        for triple in combinations(group, 3):
            triple_count += 1
            centres = [Q(*r['sigma']) for r in triple]
            all_entries = [s+e*4*n for s in centres for e in (-1,0,1)]
            if min(all_entries) <= 0 or len(set(all_entries)) != 9:
                rejected_triples += 1
                continue
            for centre_index in range(3):
                E = centres[centre_index]
                A, P = [s for i, s in enumerate(centres) if i != centre_index]
                D = 4*n
                values = (A,P+D,E-D,P-D,E,A+D,E+D,A-D,P)
                rational_roots = [rational_square_root(q) for q in values]
                denominator = lcm(*(r.denominator for r in rational_roots))
                raw_roots = tuple(int(r*denominator) for r in rational_roots)
                common_gcd = gcd(*raw_roots)
                scaling = Q(denominator, common_gcd)
                roots = canonical_by_coordinates(tuple(r//common_gcd for r in raw_roots))
                difference = D*scaling*scaling
                require(difference.denominator == 1, 'NORMALIZATION: noninteger difference')
                d = int(difference)
                require(gcd(*roots) == 1 and len(set(roots)) == 9, 'NORMALIZATION: root primitivity/distinctness')
                require(is_supported(d, primes), 'NORMALIZATION: difference support')
                common, failed, delta = line_data(roots)
                ratio = Q(abs(delta), d)
                require(ratio == abs(A+P-2*E)/D, 'NORMALIZATION: relative-defect mismatch')
                row = {'roots':list(roots),'d':d,'kernel':n,
                       'euclid':sorted([[r['m'],r['k']] for r in triple])}
                require(roots not in atlas, 'ATLAS: duplicate source triple/central role')
                atlas[roots] = row
                decorated[roots] = dict(row,common_sum=common,failed_sum=failed,delta=delta,
                                        relative_defect=[ratio.numerator,ratio.denominator])
                if minimum is None or ratio < minimum:
                    minimum = ratio
                    minima = {roots}
                elif ratio == minimum:
                    minima.add(roots)
    require(minimum is not None, 'ATLAS: no admissible array')
    class_counts = Counter(len(g) for g in groups.values())
    record = {'cutoff':cutoff,'primes':list(primes),'abc':IMPORTED_COUNTS[cutoff],
              'primitive_triangles':len(triangles),'squarefree_classes':len(groups),
              'class_size_histogram':{str(k):v for k,v in sorted(class_counts.items())},
              'midpoint_pair_tests':tests,'midpoint_hits':0,
              'unordered_triples':triple_count,'degenerate_triples':rejected_triples,
              'root_primitive_D4_arrays_9_7':len(atlas),
              'minimum_relative_defect':[minimum.numerator,minimum.denominator],
              'minimum_D4_class_count':len(minima),
              'minimum_witnesses':[decorated[k] for k in sorted(minima)]}
    return [atlas[k] for k in sorted(atlas)], record


def exact_json_equal(actual: object, expected: object) -> bool:
    """Compare JSON types as well as values (1, 1.0 and true differ)."""
    def canonical(value):
        return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)
    return canonical(actual) == canonical(expected)


def read_json(path: Path) -> object:
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f'JSON: duplicate key {key}')
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_keys)


def run(certificate_dir: Path) -> dict:
    rows = validate_abc(read_json(certificate_dir/'abc_S19.json'), 19)
    sections = []
    for cutoff in (7,13,19):
        primes = tuple(p for p in PRIMES if p <= cutoff)
        raw_subset = [list(row) for row in rows if all(is_supported(x,primes) for x in row)]
        subset = validate_abc(raw_subset,cutoff)
        triangles = triangles_by_join(subset,cutoff)
        require(exact_json_equal(triangles, read_json(certificate_dir/f'triangles_S{cutoff}.json')),
                f'TRIANGLE_ATLAS_MISMATCH: S{cutoff}')
        arrays, record = reconstruct_atlas(triangles,cutoff)
        require(exact_json_equal(arrays, read_json(certificate_dir/f'atlas_9_7_S{cutoff}.json')),
                f'ARRAY_ATLAS_MISMATCH: S{cutoff}')
        sections.append(record)
    return {'status':'PASS','claim_boundary':
            'Exact finite replay; global completeness uses imported von Kaenel--Matschke Theorem A, n=8. Not a re-proof of the imported computation.',
            'source':'arXiv:1605.06079v1, Theorem A, printed p. 7',
            'sections':sections}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificates',type=Path,default=ROOT/'certificates/smooth_support')
    ap.add_argument('--output',type=Path,default=None)
    ap.add_argument('--check-receipt',type=Path,default=ROOT/'certificates/smooth_support/expected_verification.json')
    args = ap.parse_args()
    try:
        result = run(args.certificates)
        if args.check_receipt:
            require(exact_json_equal(result, read_json(args.check_receipt)), 'RECEIPT_MISMATCH')
        text = json.dumps(result,ensure_ascii=False,indent=2)+'\n'
        if args.output:
            args.output.write_text(text,encoding='utf-8',newline='\n')
        print(text,end='')
    except (VerificationError,ValueError,OSError) as exc:
        raise SystemExit(f'FAIL: {exc}')

if __name__ == '__main__':
    main()
