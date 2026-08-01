#!/usr/bin/env python3
"""Deterministic verifier for the exact certificates of the public paper.

Re-derives, with exact integer and rational arithmetic from the Python
standard library only, the finite certificates behind the theorems of the
manuscript (block <-> paper section shown below), and checks the frozen
external-CAS records by SHA-256 digest and parsed assertions, never by
executing those systems (paper, Appendix B "certificate discipline").

  family 0  (Sec. 2)  the integral line-sum lattice: the primitive free
            relation, the exceptional mod-3 relation, determinant witnesses
            for Smith form diag(1,1,1,1,1,1,3,0), and modular ranks
  family 1  (Sec. 1)  the rationality-filter witness: Bremner's fully
            magic square of nine distinct squares over Q(sqrt3, sqrt133),
            replayed in exact quadratic-field arithmetic
  family 2  (Sec. 3, App. B)  recurrence identities, ordering, primitivity;
            the least-shift interval-analysis identities; the factor-pair
            census corroboration for n=1..6; the bridge divisor check with
            the unique (79,65,89) completion; the elliptic-orbit witnesses
            m=1 and m=3 with denominator clearing
  family 3  (Sec. 4)  the transversal interaction equation; the
            Mordell-Weil source-lock transport; the saturation certificate
            (irreducibility premises, branch divisors, degree-8 extension,
            the 30 saturated factors); the S5 monodromy certificate
  family 4  (Sec. 5.2)  the x0=841 fibre algebra, the bielliptic quotient
            identity, the pulled-back t-list, the frozen rank-0 transcript;
            a non-load-bearing PARI/GP rank-3 corroboration for the other
            quotient
  family 4b (Sec. 5.3)  the fixed Bremner-shadow quotient identity, frozen
            unconditional rank-zero result, finite-field torsion bound,
            halving test and exact elimination of every nonzero parameter
  family 5  (Sec. 5.3)  the half-class countercertificate (Q vs Q+2R and
            the 2^n family)
  family 6  (Sec. 6)  the torus identity, the nondegeneracy consequence
            table, the endpoint pigeonhole replay, the mod-8 endpoint
            table, the {2,3} exclusion replay
  family 7  (Sec. 7)  the three-block identities, the one-interior nine
            identities, the W=2x-1 forcing, the Aebi core crosscheck
  family 8  (Sec. 8)  the edge factorization and the two fixtures (area
            210, mixed 30600), the seven balanced cores and their fibres,
            the closed central and outer core-6 branches (frozen point
            lists), the six addition curves H_{n,a} and their frozen ranks
  family 9  (App. A)  the frozen (8,7) height census replayed from scratch
            as a second independent enumerator (12/13 full progressions at
            heights 46/47, unique doubled difference 840, five raw partials
            of which three survive nine-way distinctness,
            18 arrays = 9 exact D4 classes, 2 centre-nonsquare), with the
            nine canonical representatives frozen in the expected output

Engine policy: Python standard library only; no binary floating point feeds
any conclusion. One deterministic high-precision Decimal quadrature only
corroborates the displayed decimal for an analytically proved density and is
not a logical input to that theorem. External-CAS computations attributed in the paper enter as
frozen inputs and normalized output records pinned by SHA-256 below and
re-parsed here; this verifier never executes Magma or PARI/GP.  Output JSON
is byte-stable across runs and under
``python -O``; the run requires certificates/expected_verification.json and
asserts byte-identity against it.

No novelty or firstness claim; nothing here proves or refutes the
existence of a 3x3 fully magic square of nine distinct positive squares.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
CERT = PKG / "certificates"

# The pinned digest of the canonical output. The run FAILS CLOSED unless
# (a) the live output hashes to this constant, and (b) the shipped frozen
# certificate exists and is byte-identical to the live output.
EXPECTED_CERTIFICATE_SHA256 = \
    "283db3886199a93f0c510799ac70973c705f809efdba1abfa2121100747cf1b6"

D = 840  # the fixed common difference of the E840 weave


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(msg)


# --------------------------------------------------------------------------
# exact integer helpers
# --------------------------------------------------------------------------

def is_square(n: int) -> bool:
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def sqrt_exact(n: int) -> int:
    r = math.isqrt(n)
    require(r * r == n, f"{n} is not a perfect square")
    return r


def rational_sqrt(q: Fraction):
    """Exact square root of a nonnegative rational, or None."""
    if q < 0:
        return None
    num, den = q.numerator, q.denominator
    rn, rd = math.isqrt(num), math.isqrt(den)
    if rn * rn == num and rd * rd == den:
        return Fraction(rn, rd)
    return None


def icbrt(n: int) -> int:
    """Floor integer cube root for n >= 0 (integer Newton iteration)."""
    if n < 2:
        return n
    r = 1 << ((n.bit_length() + 2) // 3)
    while True:
        nr = (2 * r + n // (r * r)) // 3
        if nr >= r:
            break
        r = nr
    while r * r * r > n:
        r -= 1
    while (r + 1) ** 3 <= n:
        r += 1
    return r


def factorize(n: int) -> dict:
    """Trial-division factorization (inputs here are small or smooth)."""
    require(n != 0, "factorize(0)")
    n = abs(n)
    out: dict[int, int] = {}
    for p in (2, 3, 5, 7):
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
    f = 11
    while f * f <= n:
        while n % f == 0:
            out[f] = out.get(f, 0) + 1
            n //= f
        f += 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def merge_factors(*dicts) -> dict:
    out: dict[int, int] = {}
    for d in dicts:
        for p, e in d.items():
            out[p] = out.get(p, 0) + e
    return out


def divisors_of(fac: dict) -> list:
    divs = [1]
    for p, e in sorted(fac.items()):
        divs = [d * p**k for d in divs for k in range(e + 1)]
    return sorted(divs)


def support(n: int) -> list:
    return sorted(factorize(n))


def squarefree_signed(q: Fraction) -> int:
    """Signed squarefree part of a nonzero rational: strip small primes,
    the remaining cofactor must be a perfect square (fail-closed)."""
    require(q != 0, "squarefree part of zero")
    sign = -1 if q < 0 else 1
    n = abs(q.numerator * q.denominator)
    sf = 1
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        e = 0
        while n % p == 0:
            e += 1
            n //= p
        if e % 2:
            sf *= p
    require(is_square(n), f"squarefree part: cofactor {n} is not a square")
    return sign * sf


def vp(n: int, p: int) -> int:
    require(n != 0, "vp(0)")
    n = abs(n)
    e = 0
    while n % p == 0:
        e += 1
        n //= p
    return e


def fstr(q) -> str:
    """Canonical string for an exact rational (integers stay integers)."""
    q = Fraction(q)
    if q.denominator == 1:
        return str(q.numerator)
    return f"{q.numerator}/{q.denominator}"


def det_bareiss(a: list[list[int]]) -> int:
    """Exact determinant by fraction-free Bareiss elimination."""
    n = len(a)
    require(n > 0 and all(len(row) == n for row in a),
            "determinant requires a nonempty square matrix")
    m = [row[:] for row in a]
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot = next((r for r in range(k, n) if m[r][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            m[k], m[pivot] = m[pivot], m[k]
            sign = -sign
        p = m[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = m[i][j] * p - m[i][k] * m[k][j]
                require(numerator % previous == 0,
                        "Bareiss exact division failed")
                m[i][j] = numerator // previous
            m[i][k] = 0
        previous = p
    return sign * m[n - 1][n - 1]


def rank_mod_p(a: list[list[int]], p: int) -> int:
    """Row rank of an integer matrix over F_p."""
    require(p > 1, "rank modulus")
    m = [[x % p for x in row] for row in a]
    rows, cols = len(m), len(m[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if m[r][col]), None)
        if pivot is None:
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        inv = pow(m[rank][col], -1, p)
        m[rank] = [(inv * x) % p for x in m[rank]]
        for r in range(rows):
            if r != rank and m[r][col]:
                q = m[r][col]
                m[r] = [(x - q * y) % p
                        for x, y in zip(m[r], m[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


# --------------------------------------------------------------------------
# sparse multivariate polynomials over Q (exact)
# --------------------------------------------------------------------------

class Poly:
    __slots__ = ("n", "c")

    def __init__(self, n: int, c=None):
        self.n = n
        self.c: dict = {}
        if c:
            for k, v in c.items():
                v = Fraction(v)
                if v:
                    self.c[tuple(k)] = v

    @classmethod
    def const(cls, n, v):
        return cls(n, {(0,) * n: Fraction(v)})

    @classmethod
    def var(cls, n, i, e=1):
        k = [0] * n
        k[i] = e
        return cls(n, {tuple(k): Fraction(1)})

    def _coerce(self, other):
        if isinstance(other, Poly):
            return other
        return Poly.const(self.n, other)

    def __add__(self, other):
        other = self._coerce(other)
        out = dict(self.c)
        for k, v in other.c.items():
            w = out.get(k, Fraction(0)) + v
            if w:
                out[k] = w
            elif k in out:
                del out[k]
        p = Poly(self.n)
        p.c = out
        return p

    __radd__ = __add__

    def __neg__(self):
        p = Poly(self.n)
        p.c = {k: -v for k, v in self.c.items()}
        return p

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __rsub__(self, other):
        return self._coerce(other) + (-self)

    def __mul__(self, other):
        other = self._coerce(other)
        out: dict = {}
        for ka, va in self.c.items():
            for kb, vb in other.c.items():
                k = tuple(a + b for a, b in zip(ka, kb))
                w = out.get(k, Fraction(0)) + va * vb
                if w:
                    out[k] = w
                elif k in out:
                    del out[k]
        p = Poly(self.n)
        p.c = out
        return p

    __rmul__ = __mul__

    def __pow__(self, e: int):
        out = Poly.const(self.n, 1)
        base = self
        while e:
            if e & 1:
                out = out * base
            base = base * base
            e >>= 1
        return out

    def is_zero(self) -> bool:
        return not self.c

    def equals(self, other) -> bool:
        return (self - other).is_zero()

    def deg_in(self, i: int) -> int:
        return max((k[i] for k in self.c), default=0)

    def subst(self, i: int, val):
        """Substitute variable i by a Poly (same arity) or a rational."""
        out = Poly.const(self.n, 0)
        val_p = val if isinstance(val, Poly) else Poly.const(self.n, val)
        powers = {0: Poly.const(self.n, 1)}
        for k, coef in self.c.items():
            e = k[i]
            if e not in powers:
                powers[e] = val_p ** e
            base_k = list(k)
            base_k[i] = 0
            out = out + Poly(self.n, {tuple(base_k): coef}) * powers[e]
        return out

    def reduce_square(self, i: int, repl: "Poly") -> "Poly":
        """Rewrite var_i^2 -> repl until deg_in(i) <= 1 (used for algebraic
        relations like y^2 = f)."""
        cur = self
        while cur.deg_in(i) >= 2:
            out = Poly.const(self.n, 0)
            for k, coef in cur.c.items():
                q, r = divmod(k[i], 2)
                base_k = list(k)
                base_k[i] = r
                term = Poly(self.n, {tuple(base_k): coef})
                if q:
                    term = term * (repl ** q)
                out = out + term
            cur = out
        return cur

    def eval_at(self, vals) -> Fraction:
        tot = Fraction(0)
        for k, coef in self.c.items():
            term = coef
            for e, v in zip(k, vals):
                if e:
                    term *= Fraction(v) ** e
            tot += term
        return tot


# --------------------------------------------------------------------------
# univariate polynomial helpers (mod p, and integer resultants)
# --------------------------------------------------------------------------

def pmod(f, p):
    g = [c % p for c in f]
    while g and g[-1] == 0:
        g.pop()
    return g


def pmul(a, b, p):
    out = [0] * (len(a) + len(b) - 1) if a and b else []
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] = (out[i + j] + x * y) % p
    return pmod(out, p)


def pdivmod(a, b, p):
    a = list(a)
    binv = pow(b[-1], -1, p)
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and a:
        c = a[-1] * binv % p
        s = len(a) - len(b)
        q[s] = c
        for i, y in enumerate(b):
            a[s + i] = (a[s + i] - c * y) % p
        while a and a[-1] == 0:
            a.pop()
    return pmod(q, p), pmod(a, p)


def pgcd(a, b, p):
    a, b = pmod(a, p), pmod(b, p)
    while b:
        a, b = b, pdivmod(a, b, p)[1]
    if a:
        inv = pow(a[-1], -1, p)
        a = [c * inv % p for c in a]
    return a


def ppowmod(base, e, f, p):
    out = [1]
    b = pdivmod(base, f, p)[1]
    while e:
        if e & 1:
            out = pdivmod(pmul(out, b, p), f, p)[1]
        b = pdivmod(pmul(b, b, p), f, p)[1]
        e >>= 1
    return out


def factor_degree_pattern(f, p):
    """Degrees (descending, with multiplicity) of the irreducible factors of
    a squarefree monic-izable polynomial mod p, by distinct-degree splitting."""
    f = pmod(f, p)
    inv = pow(f[-1], -1, p)
    f = [c * inv % p for c in f]
    deriv = pmod([(i * c) % p for i, c in enumerate(f)][1:], p)
    require(len(pgcd(f, deriv, p)) == 1, f"polynomial not squarefree mod {p}")
    degrees = []
    d = 0
    while len(f) - 1 > 0:
        d += 1
        if 2 * d > len(f) - 1:
            degrees.append(len(f) - 1)
            break
        xq = ppowmod([0, 1], p ** d, f, p)          # x^(p^d) mod f
        width = max(len(xq), 2)
        diff = pmod([(xq[i] if i < len(xq) else 0) - (1 if i == 1 else 0)
                     for i in range(width)], p)
        g = pgcd(diff, f, p)
        if len(g) - 1 > 0:
            degrees.extend([d] * ((len(g) - 1) // d))
            f = pdivmod(f, g, p)[0]
    return sorted(degrees, reverse=True)


def sylvester_resultant(f, g) -> int:
    """Integer resultant via Bareiss fraction-free elimination."""
    m, n = len(f) - 1, len(g) - 1
    size = m + n
    mat = [[0] * size for _ in range(size)]
    for i in range(n):
        for j, c in enumerate(reversed(f)):
            mat[i][i + j] = c
    for i in range(m):
        for j, c in enumerate(reversed(g)):
            mat[n + i][i + j] = c
    prev = 1
    sign = 1
    for k in range(size - 1):
        if mat[k][k] == 0:
            swap = next((i for i in range(k + 1, size) if mat[i][k]), None)
            require(swap is not None, "singular Sylvester matrix")
            mat[k], mat[swap] = mat[swap], mat[k]
            sign = -sign
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                mat[i][j] = (mat[i][j] * mat[k][k] - mat[i][k] * mat[k][j]) // prev
            mat[i][k] = 0
        prev = mat[k][k]
    return sign * mat[size - 1][size - 1]


def quintic_discriminant(f) -> int:
    """disc = (-1)^(n(n-1)/2) Res(f, f') / lc(f) for n = 5."""
    fp = [i * c for i, c in enumerate(f)][1:]
    res = sylvester_resultant(f, fp)
    disc_num = res  # (-1)^10 = 1
    require(disc_num % f[-1] == 0, "discriminant division fails")
    return disc_num // f[-1]


# --------------------------------------------------------------------------
# elliptic-curve group law over Q on y^2 = x^3 + A x
# --------------------------------------------------------------------------

def ec_on(A: int, P) -> bool:
    if P is None:
        return True
    x, y = P
    return y * y == x * x * x + A * x


def ec_add(A: int, P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = Fraction(P[0]), Fraction(P[1])
    x2, y2 = Fraction(Q[0]), Fraction(Q[1])
    if x1 == x2:
        if y1 + y2 == 0:
            return None
        lam = (3 * x1 * x1 + A) / (2 * y1)
    else:
        lam = (y2 - y1) / (x2 - x1)
    x3 = lam * lam - x1 - x2
    y3 = lam * (x1 - x3) - y1
    return (x3, y3)


def ec_neg(P):
    return None if P is None else (P[0], -P[1])


def ec_mul(A: int, k: int, P):
    out = None
    base = P
    if k < 0:
        base, k = ec_neg(base), -k
    while k:
        if k & 1:
            out = ec_add(A, out, base)
        base = ec_add(A, base, base)
        k >>= 1
    return out


# --------------------------------------------------------------------------
# frozen transcript layer
# --------------------------------------------------------------------------

FROZEN_FILES = {
    # transcript / certificate outputs
    "centre841_bielliptic_fibre_magma_v2_29_8.txt":
        ("1da0876d133846b057b5a6372376246fd16f9cfcc46b87d041a657e095ffece8", 1011),
    "centre841_magma_certificate.json":
        ("358e844f66e7299214de2825a0a67a25f2ac988932374550be29efe9a72e1055", 1981),
    "centre841_first_quotient_pari_v2_17_4.txt":
        ("fd690450c8cb8296edb8e2407372d06938913bcd4424bf364daa2a411b7369b1", 307),
    "bremner_shadow_pair_quotients_pari_v2_17_4.txt":
        ("b98b2eb94932423e3cf32d46730313c5c68a5a25e9ac78bacd117c0e96808739", 1367),
    "balanced_core6_fibre_magma_v2_29_8.txt":
        ("a258dff02db3930bd4667b1dcede72aff82ed80e58bafbfdd8cc486158c92c3e", 401),
    "outer_core6_gate_magma_v2_29_8.txt":
        ("982f676075a4973f9f0bdadabddb570096ffdbfad66123f41036608c4f5c9431", 202),
    "central_addition_curves_magma_v2_29_8.txt":
        ("66025ba611161827d46331f9449c7d732434ccfe5e1fc1e077b94224c5663624", 951),
    "area30_magma.txt":
        ("54f829dba69bbd882dcbe856d7153c197e2d974434fecfb6824bf9a06e5a79b0", 141),
    "area60_magma.txt":
        ("7f2bc34e20adb1848846e81ea3bb1a1f835801abcefa576a94ffe045a1a1fdfa", 142),
    # frozen calculator inputs (byte-exact resubmission sources)
    "centre841_bielliptic_fibre.m":
        ("5b5793874481007b889ceeeac9d0897feb99714c215a9a93d13c2dc32402c57c", 1307),
    "centre841_first_quotient_pari.gp":
        ("a8e7a94dc8d9a5fe3e0a1c57343e1bae5a6e4004efc84b6ae341b8927d74e04c", 683),
    "bremner_shadow_pair_quotients.gp":
        ("5965ced8c5e3d5697922675aefe0f5c7fd0960872de62be26b363cda764eaa2a", 1521),
    "balanced_core6_fibre.m":
        ("eabb0098f55029e930959d55f8d8ebad477aac67ffd973eb828278a68a5d7994", 1077),
    "outer_core6_gate.m":
        ("aa99026e5ae46f0db40fdbeb5c1bae68eb034ae513e51076336a8dd70750d4ac", 728),
    "central_addition_curves.m":
        ("5a4f7d179b222d01b9dbee34894e9ce4a5aa7ab474c4bd5776e80234ffc6573a", 1308),
    "addition_curve_full_class_area30.m":
        ("74cbed6c9ef1284ddbe4294bcefcae0c2502e70d7f0407d6d644ec62f3861c5b", 350),
    "addition_curve_full_class_area60.m":
        ("84cdb031d7369fe20e697840d3a35e266c0da33abc075ff143859b8412ec96c9", 354),
}

_KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]*(?:\s|$)")


def load_frozen(name: str) -> bytes:
    path = CERT / name
    require(path.exists(), f"missing frozen file {name}")
    data = path.read_bytes()
    sha, size = FROZEN_FILES[name]
    require(len(data) == size, f"{name}: {len(data)} bytes, expected {size}")
    got = hashlib.sha256(data).hexdigest()
    require(got == sha, f"{name}: sha256 {got} != frozen {sha}")
    return data


def parse_transcript(text: str) -> dict:
    """Normalize KEY VALUE records; continuation lines (pretty-printer wraps
    and bracket blocks) are re-joined onto the last KEY."""
    records = []
    cur = None
    depth = 0
    for raw in text.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            continue
        opens = sum(line.count(c) for c in "[{(")
        closes = sum(line.count(c) for c in "]})")
        if depth == 0 and _KEY_RE.match(line):
            if cur is not None:
                records.append(cur)
            cur = line.strip()
        else:
            require(cur is not None, "transcript starts with a continuation")
            cur += " " + line.strip()
        depth += opens - closes
    if cur is not None:
        records.append(cur)
    out: dict[str, list] = {}
    order = []
    for rec in records:
        parts = rec.split(None, 1)
        key = parts[0]
        val = parts[1].strip() if len(parts) > 1 else ""
        out.setdefault(key, []).append(val)
        order.append((key, val))
    out["__order__"] = order
    return out


def t_value(rec: dict, key: str) -> str:
    require(key in rec and len(rec[key]) == 1, f"transcript key {key} missing/dup")
    return rec[key][0]


def parse_int_list(s: str) -> list:
    body = s.strip()
    require(body.startswith("[") and body.endswith("]"), f"not a list: {s}")
    inner = body[1:-1].strip()
    if not inner:
        return []
    return [Fraction(tok.strip()) for tok in inner.split(",")]


# --------------------------------------------------------------------------
# family 0 -- Section 2: integral lattice of the eight line sums
# --------------------------------------------------------------------------

def family0_line_sum_lattice(emit) -> dict:
    matrix = [
        [1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 1, 0, 1, 0, 1, 0, 0],
    ]

    def left_product(v):
        return [sum(v[r] * matrix[r][c] for r in range(8))
                for c in range(9)]

    free_relation = [-1, -1, -1, 1, 1, 1, 0, 0]
    mod3_relation = [1, 0, 1, 0, -1, 0, -1, -1]
    require(left_product(free_relation) == [0] * 9,
            "primitive free line-sum relation")
    require(left_product(mod3_relation) == [0, 0, 0, 0, -3, 0, 0, 0, 0],
            "exceptional mod-3 line-sum relation")

    rows6, cols6 = [0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 5, 6]
    rows7, cols7 = [0, 1, 2, 3, 4, 6, 7], list(range(7))
    minor6 = [[matrix[r][c] for c in cols6] for r in rows6]
    minor7 = [[matrix[r][c] for c in cols7] for r in rows7]
    det6, det7 = det_bareiss(minor6), det_bareiss(minor7)
    require(det6 == -1 and det7 == -3,
            "Smith determinant witnesses")
    ranks = {str(p): rank_mod_p(matrix, p) for p in (2, 3, 5, 7)}
    require(ranks == {"2": 7, "3": 6, "5": 7, "7": 7},
            "line-sum modular ranks")

    # The free relation bounds the rational rank by seven and det7 != 0
    # gives equality. Since rank mod 3 is six, every 7-minor is divisible
    # by 3; det7=-3 makes their gcd exactly 3. The unit 6-minor fixes all
    # preceding invariant factors. These are the determinantal-divisor
    # data for the asserted Smith form.
    smith = [1, 1, 1, 1, 1, 1, 3, 0]
    emit("family0: line-sum lattice certified exactly -- Smith form "
         "diag(1,1,1,1,1,1,3,0), cokernel Z plus Z/3Z, unique "
         "exceptional characteristic 3")
    return {
        "matrix": matrix,
        "rank_over_Q": 7,
        "smith_form": smith,
        "cokernel": "Z direct-sum Z/3Z",
        "free_relation": free_relation,
        "mod3_relation": mod3_relation,
        "minor6": {"rows_zero_based": rows6,
                   "columns_zero_based": cols6, "determinant": det6},
        "minor7": {"rows_zero_based": rows7,
                   "columns_zero_based": cols7, "determinant": det7},
        "image_conditions": [
            "R1+R2+R3=C1+C2+C3",
            "R1+R3=C2+Dplus+Dminus (mod 3)",
        ],
        "ranks_mod_p": ranks,
        "exceptional_prime": 3,
    }


# --------------------------------------------------------------------------
# family 1 -- Section 1: the rationality-filter witness (Bremner's square
# over Q(sqrt3, sqrt133)); everything else in Sections 1-2 is historical or
# proved in prose with no computational content to replay.
# --------------------------------------------------------------------------

def family1_quartic_witness(emit) -> dict:
    """Exact replay of the degree-four witness promised in Section 1: a
    fully magic square of nine distinct squares over Q(sqrt3, sqrt133).
    The square is Bremner's (BRE01; the degree-4 realization recorded in
    the project state of the art); arithmetic in Q(sqrt3) is exact pairs
    (a, b) = a + b*sqrt(3)."""
    def mul(x, y):
        return (x[0] * y[0] + 3 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    def add(x, y):
        return (x[0] + y[0], x[1] + y[1])

    roots = [[(5, -13), (17, 9), (22, -4)],
             [(23, -1), None, (23, 1)],
             [(22, 4), (17, -9), (5, 13)]]
    centre = (532, 0)  # = (2*sqrt(133))^2 = 4*133
    require(4 * 133 == 532, "centre is the square of 2*sqrt(133)")
    grid = [[centre if r is None else mul(r, r) for r in row]
            for row in roots]
    entries = [v for row in grid for v in row]
    require(len(set(entries)) == 9, "witness distinctness")
    target = (1596, 0)
    lines = ([[grid[i][j] for j in range(3)] for i in range(3)] +
             [[grid[i][j] for i in range(3)] for j in range(3)] +
             [[grid[0][0], grid[1][1], grid[2][2]],
              [grid[0][2], grid[1][1], grid[2][0]]])
    for line in lines:
        tot = (0, 0)
        for v in line:
            tot = add(tot, v)
        require(tot == target, "witness line sum 1596")
    # the field really has degree four: 3, 133 and 3*133 = 399 are all
    # nonsquares, so Q(sqrt3, sqrt133) / Q is biquadratic
    require(not is_square(3) and not is_square(133) and not is_square(399),
            "biquadratic degree certificate")
    require(squarefree_signed(Fraction(133)) == 133, "133 squarefree")
    emit("family1: Bremner's quartic-field witness replayed exactly -- "
         "nine distinct squares over Q(sqrt3, sqrt133), all eight lines "
         "sum 1596, centre 532 = (2 sqrt133)^2")
    return {
        "attribution": "Bremner (BRE01); exact replay only",
        "field": "Q(sqrt3, sqrt133), biquadratic of degree 4",
        "centre": 532,
        "magic_sum": 1596,
        "entries_a_plus_b_sqrt3": [[list(v) for v in row] for row in grid],
        "distinct_entries": 9,
    }


# --------------------------------------------------------------------------
# family 2 -- Section 3: the three construction mechanisms
# --------------------------------------------------------------------------

def orbit_xyz(n_max: int):
    seq = [(3, 1, 1)]
    for _ in range(n_max):
        x, y, z = seq[-1]
        seq.append((3 * x + 2 * z, x, x + z))
    return seq  # seq[n] = (x_n, y_n, z_n)


def family2_retraction(emit) -> dict:
    n = 2  # variables y, z
    y, z = Poly.var(n, 0), Poly.var(n, 1)
    x = y + 2 * z
    inv_repl = 1 + 2 * z * z - 2 * y * z          # y^2 == this on the family

    def zero_mod_inv(p: Poly) -> bool:
        return p.reduce_square(0, inv_repl).is_zero()

    # the three retraction identities of Sec. 3.1
    idC = (x * x + y * y * z * z - 6 * z * z) - (y * z + 1) ** 2
    idG = (x * x * z * z + y * y - 6 * z * z) - (x * z - 1) ** 2
    idE = (x * x + y * y) * (z * z + 1) - 12 * z * z - 2 * (
        4 * z ** 4 - z * z + 1)
    require(zero_mod_inv(idC) and zero_mod_inv(idG) and zero_mod_inv(idE),
            "retraction identities fail")

    # N_n line sums: seven lines at 3(4z^4+3z^2+1), antidiagonal at
    # 3(4z^4-z^2+1) -- checked as polynomial identities mod the invariant
    cells = [[(x * y - z) ** 2, (x * z + y) ** 2, (y * z + 1) ** 2],
             [(x + y * z) ** 2, 4 * z ** 4 - z * z + 1, (x * z - y) ** 2],
             [(x * z - 1) ** 2, (y * z - x) ** 2, (x * y + z) ** 2]]
    s7 = 3 * (4 * z ** 4 + 3 * z * z + 1)
    sA = 3 * (4 * z ** 4 - z * z + 1)
    lines = ([[cells[i][j] for j in range(3)] for i in range(3)] +
             [[cells[i][j] for i in range(3)] for j in range(3)] +
             [[cells[0][0], cells[1][1], cells[2][2]]])
    for k, line in enumerate(lines):
        require(zero_mod_inv(sum(line, Poly.const(n, 0)) - s7),
                f"line {k} sum fails")
    anti = cells[0][2] + cells[1][1] + cells[2][0]
    require(zero_mod_inv(anti - sA), "antidiagonal sum fails")
    require((s7 - sA).equals(12 * z * z), "defect != 12z^2")

    # centre window (nonsquare for z>1)
    require(((4 * z ** 4 - z * z + 1) - (2 * z * z - 1) ** 2).equals(3 * z * z),
            "centre lower window")
    require(((2 * z * z) ** 2 - (4 * z ** 4 - z * z + 1)).equals(z * z - 1),
            "centre upper window")

    # gap identities (mod invariant) + their lower-bound factorizations
    gap1 = ((x * y - z) - (x + y * z)) - (2 * z * z - y * z - y - 3 * z + 1)
    require(zero_mod_inv(gap1), "gap1 identity")
    require(((2 * z * z - y * z - y - 3 * z + 1) - (z - 1) * (z - 2))
            .equals((z + 1) * (z - 1 - y)), "gap1 bound factorization")
    gap2 = ((x * z - y) - (x * y + z)) - ((y - 1) * (z - 1) - 2)
    require(zero_mod_inv(gap2), "gap2 identity")
    require(((y * z - x) - (y * (z - 1) - 2 * z)).is_zero(), "first-root form")
    require(((y * z + 1) - (y * z - x) - (x + 1)).is_zero(), "x+1 difference")
    require(((x + y * z) - (y * z + 1) - (x - 1)).is_zero(), "x-1 difference")

    # distinguished CG pair at t0 = 6z^2 and the universal all-square shift
    delta = 2 * z * (y + z) * (z * z - 1)
    d0, e0 = 2 * (z * z - 1), 2 * z * (y + z)
    require((d0 * e0 - 2 * delta).is_zero(), "CG pair product")
    require(((e0 - d0) - 2 * (y * z + 1)).is_zero(), "CG pair u")
    require(zero_mod_inv((e0 + d0) - 2 * (x * z - 1)), "CG pair v")
    C_p = x * x + y * y * z * z
    G_p = x * x * z * z + y * y
    E2_p = (x * x + y * y) * (z * z + 1)          # 2E
    require((C_p - 2 * x * y * z - (y * z - x) ** 2).is_zero(), "deg shift C")
    require(zero_mod_inv(E2_p - 4 * x * y * z - 2 * (x * y - z) ** 2),
            "deg shift E")
    require((G_p - 2 * x * y * z - (x * z - y) ** 2).is_zero(), "deg shift G")

    # interval-analysis identities (Appendix B)
    yn, zn = y + 2 * z, y + 3 * z              # the (y,z) recurrence step
    require((zn - yn).equals(z), "red z-y")
    require((2 * yn - zn).equals(y + z), "red 2y-z")
    require((5 * yn - 3 * zn).equals(2 * y + z), "red 5y-3z")
    require((5 * zn - 6 * yn).equals(3 * z - y), "red 5z-6y")
    require((8 * yn - 5 * zn).equals(3 * y + z), "red 8y-5z")
    require(((10 * y * z + 35 - 6 * z * z) - (2 * z * (5 * y - 3 * z) + 35))
            .is_zero(), "C-entry bound identity")
    X_p = y * z + 2 * z * z - 1                # X = xz-1 on the family
    require(zero_mod_inv(x * z - 1 - X_p), "X normal form")
    require(((4 * X_p + 4 - 6 * z * z) - 2 * z * (2 * y + z)).is_zero(),
            "G-entry bound identity")
    H_p = 4 * z ** 4 - z * z + 1
    require((H_p - (2 * z * z - 1) ** 2).equals(3 * z * z), "E win 1")
    require(((2 * z * z) ** 2 - H_p).equals(z * z - 1), "E win 2")
    require((H_p + 6 * z * z - (2 * z * z + 1) ** 2).equals(z * z), "E win 3")
    require(((2 * z * z + 2) ** 2 - (H_p + 6 * z * z)).equals(3 * z * z + 3),
            "E win 4")
    Y_p = y * z + 1
    for a in (1, 2, 3, 4):
        lhs = a * (2 * Y_p + a)
        require(((z * z - 1) - lhs - (z * (z - 2 * a * y) - (a + 1) ** 2))
                .is_zero(), f"CE col1 a={a}")
        require((5 * z * z - lhs - (z * (5 * z - 2 * a * y) - a * (a + 2)))
                .is_zero(), f"CE col2 a={a}")
    cg_expect = {1: 4 * z * z - 4, 2: 2 * z * (2 * z - y) - 9,
                 3: 4 * (z * (z - y) - 4), 4: 2 * z * (2 * z - 3 * y) - 25}
    for a in (1, 2, 3, 4):
        require(((2 * X_p + 1) - a * (2 * Y_p + a) - cg_expect[a]).is_zero(),
                f"CG a={a}")
    require(((2 * X_p + 1) - (z * z - 1) - (2 * y * z + 3 * z * z)).is_zero(),
            "EG vs z^2-1")
    require(((2 * X_p + 1) - 5 * z * z - (z * (2 * y - z) - 1)).is_zero(),
            "EG vs 5z^2")

    # numeric corroboration along the orbit
    orbit = orbit_xyz(20)
    roots_gcds = []
    for nn in range(1, 21):
        xv, yv, zv = orbit[nn]
        require(xv - yv == 2 * zv and yv * yv + 2 * yv * zv - 2 * zv * zv == 1,
                f"invariants fail at n={nn}")
        require(xv % 2 == 1 and yv % 2 == 1, "x,y parity")
        roots = [yv * zv - xv, yv * zv + 1, xv + yv * zv, xv * yv - zv,
                 xv * yv + zv, xv * zv - yv, xv * zv - 1, xv * zv + yv]
        require(all(r > 0 for r in roots), f"positivity n={nn}")
        require(all(roots[i] < roots[i + 1] for i in range(7)),
                f"ordering n={nn}")
        g = 0
        for r in roots:
            g = math.gcd(g, r)
        roots_gcds.append(g)
        require(g == (1 if nn % 2 == 1 else 2), f"root gcd n={nn}")
        entries = [(xv * yv - zv) ** 2, (xv * zv + yv) ** 2,
                   (yv * zv + 1) ** 2, (xv + yv * zv) ** 2,
                   4 * zv ** 4 - zv * zv + 1, (xv * zv - yv) ** 2,
                   (xv * zv - 1) ** 2, (yv * zv - xv) ** 2,
                   (xv * yv + zv) ** 2]
        require(len(set(entries)) == 9, f"distinctness n={nn}")
        if nn >= 2:
            yv2, zv2 = yv, zv
            require(zv2 > yv2 and 2 * yv2 > zv2 and 5 * yv2 > 3 * zv2
                    and 5 * zv2 > 6 * yv2 and 8 * yv2 > 5 * zv2 and zv2 >= 15,
                    f"induction inequalities n={nn}")
            require(zv2 * (5 * zv2 - 6 * yv2) > 15, f"CE row3 exclusion n={nn}")

    # least shift at n=1: windows for 1<=t<=8, closure at t=9
    Cv, Ev, Gv = 265, 1105, 1945
    for t in range(1, 9):
        require(16 ** 2 < Cv - t < 17 ** 2, "n=1 C window")
        require(33 ** 2 < Ev - t < 34 ** 2, "n=1 E window")
        require(44 ** 2 < Gv - t < 45 ** 2, "n=1 G window")
    require((Cv - 9, Ev - 9, Gv - 9) == (256, 1096, 1936)
            and is_square(256) and is_square(1936) and not is_square(1096),
            "n=1 closure at t=9")

    # factor-pair census replay for n=1..6 against the frozen table
    frozen_rows = {
        1: (11, 3, 4, 840, 96, 264, 2, 3, 1, 4, 3),
        2: (41, 11, 15, 174720, 1350, 13530, 6, 5, 1, 10, 9),
        3: (153, 41, 56, 34058640, 18816, 702576, 9, 8, 2, 17, 16),
        4: (571, 153, 209, 6609482880, 262086, 36517734, 28, 22, 4, 52, 51),
        5: (2131, 571, 780, 1282237396440, 3650400, 1898209560, 33, 32, 4,
            67, 66),
        6: (7953, 2131, 2911, 248747888014080, 50843526, 98670341946, 44, 35,
            6, 83, 82),
    }
    census = {}
    for nn in range(1, 7):
        xv, yv, zv = orbit[nn]
        Cn = xv * xv + yv * yv * zv * zv
        En = (xv * xv + yv * yv) * (zv * zv + 1) // 2
        Gn = xv * xv * zv * zv + yv * yv
        Dn = En - Cn
        require(Gn - En == Dn, "arithmetic progression C,E,G")
        fac_D = merge_factors(factorize(2), factorize(zv),
                              factorize(yv + zv), factorize(zv - 1),
                              factorize(zv + 1))
        require(Dn == 2 * zv * (yv + zv) * (zv * zv - 1), "Delta closed form")
        divs_D = divisors_of(fac_D)
        divs_2D = divisors_of(merge_factors(fac_D, {2: 1}))
        ce, cg, eg = set(), set(), set()
        for dlist, target, out in ((divs_D, Dn, ce), (divs_2D, 2 * Dn, cg)):
            for dd in dlist:
                ee = target // dd
                if dd >= ee or (dd - ee) % 2:
                    continue
                u = (ee - dd) // 2
                t = Cn - u * u
                if 0 < t < Cn:
                    out.add(t)
        for dd in divs_D:
            ee = Dn // dd
            if dd >= ee or (dd - ee) % 2:
                continue
            w = (ee - dd) // 2
            t = En - w * w
            if 0 < t < Cn:
                eg.add(t)
        allt = ce | cg | eg
        deg = 2 * xv * yv * zv
        nondeg = sorted(allt - {deg})
        row = frozen_rows[nn]
        require((row[0], row[1], row[2]) == (xv, yv, zv), f"orbit row n={nn}")
        require(Dn == row[3], f"Delta n={nn}")
        require(6 * zv * zv == row[4], f"t0 n={nn}")
        require(deg == row[5], f"all-square shift n={nn}")
        require((len(ce), len(cg), len(eg)) == (row[6], row[7], row[8]),
                f"branch counts n={nn}: {(len(ce), len(cg), len(eg))}")
        require(len(allt) == row[9] and len(nondeg) == row[10],
                f"census totals n={nn}")
        require(deg in ce and deg in cg and deg in eg,
                f"degenerate shift in all branches n={nn}")
        tmin = min(allt)
        require(tmin == (9 if nn == 1 else 6 * zv * zv), f"t_min n={nn}")
        if nn >= 2:
            require(6 * zv * zv in cg, f"t0 realized as CG n={nn}")
        census[str(nn)] = {"t_min": tmin, "branch_counts":
                           [len(ce), len(cg), len(eg)],
                           "distinct_shifts": len(allt)}
        if nn == 2:
            require(sorted(allt) == [1350, 13530, 16137, 20442, 23130, 25542,
                                     26697, 27882, 28065, 28902],
                    "n=2 full shift list")
            grid = [[190096, 391876, 12769], [42436, 187489, 364816],
                    [362209, 15376, 217156]]
            xv2, yv2, zv2 = orbit[2]
            w2 = [[(xv2 * yv2 - zv2) ** 2, (xv2 * zv2 + yv2) ** 2,
                   xv2 * xv2 + yv2 * yv2 * zv2 * zv2],
                  [(xv2 + yv2 * zv2) ** 2,
                   (xv2 * xv2 + yv2 * yv2) * (zv2 * zv2 + 1) // 2,
                   (xv2 * zv2 - yv2) ** 2],
                  [xv2 * xv2 * zv2 * zv2 + yv2 * yv2,
                   (yv2 * zv2 - xv2) ** 2, (xv2 * yv2 + zv2) ** 2]]
            t = 16137
            for (i, j) in ((0, 2), (1, 1), (2, 0)):
                w2[i][j] -= t
            require(w2 == grid, "n=2 counterexample grid")
            sums = ([sum(r) for r in w2] + [sum(c) for c in zip(*w2)]
                    + [w2[0][0] + w2[1][1] + w2[2][2],
                       w2[0][2] + w2[1][1] + w2[2][0]])
            require(sums.count(594741) == 7 and sums.count(562467) == 1,
                    "n=2 counterexample line sums")
    emit("family2: retraction identities, interval analysis and census "
         "replayed (n=1..6; t_min = 9, then 6z^2)")
    return {
        "identities_mod_invariant": True,
        "interval_analysis_identities": True,
        "census": census,
        "root_gcd_pattern_n1_20": roots_gcds,
    }


def family2_bridge(emit) -> dict:
    # the type-6.VI normalized grid is fully magic as a polynomial identity
    n = 3
    A_, N_, Z_ = (Poly.var(n, i) for i in range(3))
    M = [[2 * N_ - Z_, A_, N_ - A_ + Z_],
         [2 * Z_ - A_, N_, 2 * N_ - 2 * Z_ + A_],
         [N_ + A_ - Z_, 2 * N_ - A_, Z_]]
    target = 3 * N_
    all_lines = ([[M[i][j] for j in range(3)] for i in range(3)] +
                 [[M[i][j] for i in range(3)] for j in range(3)] +
                 [[M[0][0], M[1][1], M[2][2]],
                  [M[0][2], M[1][1], M[2][0]]])
    for line in all_lines:
        require((sum(line, Poly.const(n, 0)) - target).is_zero(),
                "6.VI magic identity")
    # antidiagonal is (N-delta, N, N+delta) with delta = A - Z
    delta_p = A_ - Z_
    require((M[0][2] - (N_ - delta_p)).is_zero()
            and (M[2][0] - (N_ + delta_p)).is_zero(), "antidiagonal AP form")

    # bridge (23,37,47): delta=840, factor pairs of 2*delta=1680
    dd, zz, aa = 23, 37, 47
    delta = aa * aa - zz * zz
    require(delta == zz * zz - dd * dd == 840, "bridge differences")
    completions = []
    for u in divisors_of(factorize(2 * delta)):
        v = 2 * delta // u
        if u >= v or (u - v) % 2:
            continue
        b = (v - u) // 2
        c = (v + u) // 2
        n2, rem = divmod(aa * aa + b * b, 2)
        if rem:
            continue
        if is_square(n2):
            nn = sqrt_exact(n2)
            require(dd * dd + c * c == 2 * n2, "centre relation")
            completions.append((u, v, b, nn, c))
    require(completions == [(10, 168, 79, 65, 89), (24, 70, 23, 37, 47)],
            f"bridge completions: {completions}")
    tautological = completions[1]
    admissible = completions[0]
    require(tautological[2:] == (23, 37, 47), "tautological completion")
    require(admissible[2:] == (79, 65, 89), "unique admissible completion")

    # the resulting carrier + Robertson retraction -> the explicit array
    Av, Nv, Zv = 47 ** 2, 65 ** 2, 37 ** 2
    M0 = [[2 * Nv - Zv, Av, Nv - Av + Zv],
          [2 * Zv - Av, Nv, 2 * Nv - 2 * Zv + Av],
          [Nv + Av - Zv, 2 * Nv - Av, Zv]]
    require(M0 == [[7081, 2209, 3385], [529, 4225, 7921],
                   [5065, 6241, 1369]], "M0 reconstruction")
    tau = 65 ** 2 - 29 ** 2
    require(tau == 3384, "tau")
    out = [row[:] for row in M0]
    for (i, j) in ((0, 2), (1, 1), (2, 0)):
        out[i][j] -= tau
    require(out == [[7081, 2209, 1], [529, 841, 7921], [1681, 6241, 1369]],
            "bridge output array")
    sums = ([sum(r) for r in out] + [sum(c) for c in zip(*out)]
            + [out[0][0] + out[1][1] + out[2][2],
               out[0][2] + out[1][1] + out[2][0]])
    require(sums.count(9291) == 7 and sums.count(2523) == 1,
            "bridge array line sums")
    nonsquares = [v for row in out for v in row if not is_square(v)]
    require(nonsquares == [7081], "unique nonsquare")
    require(len({v for row in out for v in row}) == 9, "bridge distinctness")
    require(all(v > 0 for row in out for v in row), "bridge positivity")
    emit("family2: bridge divisor check -- completions of 2*840 are exactly "
         "the tautological (23,37,47) and (79,65,89); array sum 9291")
    return {
        "delta": delta,
        "completions": [list(c) for c in completions],
        "array": out,
        "seven_line_sum": 9291,
        "failed_antidiagonal_sum": 2523,
    }


M0_CARRIER = [[7081, 2209, 3385], [529, 4225, 7921], [5065, 6241, 1369]]
OUTSIDE_ROOTS = [23, 37, 47, 79, 89]
A840 = -(D * D)  # y^2 = x^3 - 840^2 x


def lift_witness(m: int, P) -> dict:
    """Replay the fixed-carrier lift at the point m*P (P = 2Q)."""
    R = ec_mul(A840, m, P)
    x = Fraction(R[0])
    require(D < x < 65 ** 2, f"witness m={m} outside window")
    roots = []
    for shift in (-D, 0, D):
        r = rational_sqrt(x + shift)
        require(r is not None and r > 0, f"witness m={m}: root not rational")
        roots.append(r)
    lam = 1
    for r in roots:
        lam = lam * r.denominator // math.gcd(lam, r.denominator)
    cleared = [int(r * lam) for r in roots]
    require(all(Fraction(c, lam) == r for c, r in zip(cleared, roots)),
            "cleared roots")
    tau = (65 ** 2 - x) * lam * lam
    require(tau.denominator == 1 and tau > 0, "tau integral")
    tau = int(tau)
    grid = [[v * lam * lam for v in row] for row in M0_CARRIER]
    for (i, j) in ((0, 2), (1, 1), (2, 0)):
        grid[i][j] -= tau
    require(grid[0][2] == cleared[0] ** 2 and grid[1][1] == cleared[1] ** 2
            and grid[2][0] == cleared[2] ** 2, "antidiagonal squares")
    entries = [v for row in grid for v in row]
    require(all(v > 0 for v in entries), "positivity")
    require(len(set(entries)) == 9, "distinctness")
    sq = [v for v in entries if is_square(v)]
    require(len(sq) == 8 and not is_square(grid[0][0]), "eight squares")
    require(grid[0][0] == 7081 * lam * lam, "nonsquare = 7081*lambda^2")
    scaled_outside = [r * lam for r in OUTSIDE_ROOTS]
    require(not (set(cleared) & set(scaled_outside)), "roots avoid carrier")
    g = 0
    for v in entries:
        g = math.gcd(g, v)
    require(g == 1, "entry primitivity")
    rg = math.gcd(math.gcd(cleared[0], cleared[1]), cleared[2])
    lines = ([sum(r) for r in grid] + [sum(c) for c in zip(*grid)]
             + [grid[0][0] + grid[1][1] + grid[2][2]])
    anti = grid[0][2] + grid[1][1] + grid[2][0]
    require(len(set(lines)) == 1, "seven common lines")
    require(anti == lines[0] - 2 * tau, "defect = 2*tau")
    return {
        "m": m,
        "x": fstr(x),
        "lambda": lam,
        "roots": [fstr(r) for r in roots],
        "cleared_roots": cleared,
        "shift_tau": tau,
        "output_grid": grid,
        "common_line_sum": lines[0],
        "failed_diagonal_sum": anti,
        "entry_gcd": g,
        "cleared_root_gcd": rg,
    }


def density_decimal_certificate() -> dict:
    """Deterministic corroboration of the displayed density decimal.

    The theorem uses the exact Haar-measure/incomplete-beta expression.
    This routine merely checks its printed decimal after the regularizing
    substitution t=1-u^2, using two composite-Simpson resolutions.
    """
    with localcontext() as ctx:
        ctx.prec = 60
        one = Decimal(1)
        lower_t = (Decimal(840) / Decimal(4225)).sqrt()
        numerator_endpoint = (one - lower_t).sqrt()

        def integrand(u: Decimal) -> Decimal:
            u2 = u * u
            radicand = Decimal(4) - Decimal(6) * u2 \
                + Decimal(4) * u2 * u2 - u2 * u2 * u2
            return Decimal(2) / radicand.sqrt()

        def simpson(endpoint: Decimal, panels: int) -> Decimal:
            require(panels > 0 and panels % 2 == 0,
                    "Simpson panel count")
            h = endpoint / Decimal(panels)
            total = integrand(Decimal(0)) + integrand(endpoint)
            for k in range(1, panels):
                total += Decimal(4 if k % 2 else 2) * integrand(h * k)
            return total * h / Decimal(3)

        values = []
        for panels in (4096, 8192):
            values.append(simpson(numerator_endpoint, panels)
                          / simpson(one, panels))
        require(abs(values[1] - values[0]) < Decimal("3e-17"),
                "density quadrature resolutions disagree")
        require(format(values[1], ".16f") == "0.6585271498271213",
                "displayed density decimal")
        beta_argument = Fraction(840, 4225) ** 2
        require(beta_argument == Fraction(28224, 714025),
                "density beta argument reduction")
        return {
            "exact_expression": "1-I_(28224/714025)(1/4,1/2)",
            "beta_argument": fstr(beta_argument),
            "beta_parameters": ["1/4", "1/2"],
            "decimal_16": format(values[1], ".16f"),
            "simpson_panels": [4096, 8192],
            "coarse_decimal": format(values[0], ".20f"),
            "fine_decimal": format(values[1], ".20f"),
            "logical_role": "numerical corroboration only",
        }


def family2_lift(emit) -> dict:
    # doubling identities (EL-1), reduced modulo v^2 = u^3 - 840^2 u
    n = 2
    u, v = Poly.var(n, 0), Poly.var(n, 1)
    v2 = u ** 3 - D * D * u

    def red(p):
        return p.reduce_square(1, v2)

    require(red((u * u + D * D) ** 2
                - ((3 * u * u - D * D) ** 2 - 8 * u * v * v)).is_zero(),
            "doubling x identity")
    require(red((u * u - 2 * D * u - D * D) ** 2
                - ((u * u + D * D) ** 2 - 4 * D * v * v)).is_zero(),
            "doubling x-840 identity")
    require(red((u * u + 2 * D * u - D * D) ** 2
                - ((u * u + D * D) ** 2 + 4 * D * v * v)).is_zero(),
            "doubling x+840 identity")

    Q = (Fraction(1960), Fraction(78400))
    require(ec_on(A840, Q), "Q on curve")
    P = ec_add(A840, Q, Q)
    require(P == (Fraction(841), Fraction(-1189)), "P = 2Q")

    # Lutz--Nagell certificate
    ln = 4 * D ** 6
    require(ln == 1405192126464000000 and support(ln) == [2, 3, 5, 7],
            "Lutz-Nagell divisor")
    require(1189 == 29 * 41 and ln % (1189 * 1189) != 0,
            "1189^2 does not divide 4*840^6")
    counts = {}
    for p in (11, 13):
        cnt = 1  # infinity
        for xv in range(p):
            rhs = (xv ** 3 + A840 * xv) % p
            cnt += sum(1 for yv in range(p) if (yv * yv - rhs) % p == 0)
        counts[p] = cnt
    require(counts[11] == 12 and counts[13] == 20, "good-reduction counts")
    require(math.gcd(12, 20) == 4, "torsion bound gcd")
    require(P[1] != 0, "P not two-torsion")

    w1 = lift_witness(1, P)
    require(w1["lambda"] == 1 and w1["cleared_roots"] == [1, 29, 41]
            and w1["shift_tau"] == 3384
            and w1["output_grid"] == [[7081, 2209, 1], [529, 841, 7921],
                                      [1681, 6241, 1369]]
            and w1["common_line_sum"] == 9291
            and w1["failed_diagonal_sum"] == 2523, "witness m=1")
    w3 = lift_witness(3, P)
    require(w3["lambda"] == 1991476962717, "witness m=3 lambda")
    require(w3["x"] == "3367288018268977161721428361/"
            "3965980493032527408022089", "witness m=3 x")
    require(w3["cleared_roots"] == [5988689683199, 58028338062269,
                                    81845657382761], "witness m=3 roots")
    require(w3["shift_tau"] == 13388979564793451137171897664,
            "witness m=3 shift")
    require(w3["output_grid"] == [
        [28083107871163326576204412209, 8760850909108853044320794601,
         35864404121654138982873601],
        [2098003680814206998843685081, 3367288018268977161721428361,
         31414531485310649598942966969],
        [6698711632416300184459983121, 24751684257016003553465857449,
         5429427294961530021582239841]], "witness m=3 grid")
    require(w3["common_line_sum"] == 36879823184393833759508080411
            and w3["failed_diagonal_sum"] == 10101864054806931485164285083,
            "witness m=3 sums")
    require(w1["x"] != w3["x"], "witness centres distinct")

    in_window = []
    for m in range(1, 13):
        xm = ec_mul(A840, m, P)[0]
        if D < xm < 65 ** 2:
            in_window.append(m)
    require(in_window == [1, 3, 5, 7, 9, 11], "bounded window diagnostic")
    density = density_decimal_certificate()
    emit("family2: elliptic-orbit witnesses m=1 and m=3 recomputed exactly "
         f"(lambda_3 = {w3['lambda']}); window indices {in_window}; "
         f"density decimal {density['decimal_16']} corroborated")
    return {
        "doubling_identities": True,
        "lutz_nagell": {"divisor": ln, "support": [2, 3, 5, 7],
                        "orders": {"11": 12, "13": 20}, "gcd_bound": 4},
        "witnesses": [w1, w3],
        "window_indices_m_le_12": in_window,
        "return_density": {
            "counting_law": "A(N)=delta*N+o(N)",
            "window": [840, 4225],
            **density,
        },
    }


# --------------------------------------------------------------------------
# family 3 -- Section 4: interaction surface, saturation, S5 wall
# --------------------------------------------------------------------------

def family3(emit) -> dict:
    # (i) the transversal equation
    n = 3
    x0, x1, x2 = (Poly.var(n, i) for i in range(3))
    grid = [[x1, x2 + D, x0 - D],
            [x2 - D, x0, x1 + D],
            [x0 + D, x1 - D, x2]]
    tot = x0 + x1 + x2
    lines = ([[grid[i][j] for j in range(3)] for i in range(3)] +
             [[grid[i][j] for i in range(3)] for j in range(3)] +
             [[grid[0][0], grid[1][1], grid[2][2]]])
    for line in lines:
        require((sum(line, Poly.const(n, 0)) - tot).is_zero(),
                "transversal seven-line identity")
    anti = grid[0][2] + grid[1][1] + grid[2][0]
    require((anti - 3 * x0).is_zero(), "transversal antidiagonal")
    require((tot - anti - (x1 + x2 - 2 * x0)).is_zero(),
            "interaction defect identity")

    # Mordell-Weil source lock: LMFDB 705600.vn3 -> (Q, R)
    A_min = -44100
    g1 = (Fraction(-84), Fraction(-1764))
    g2 = (Fraction(294), Fraction(3528))
    require(ec_on(A_min, g1) and ec_on(A_min, g2), "minimal-model generators")
    img1 = (4 * g1[0], 8 * g1[1])
    img2 = (4 * g2[0], 8 * g2[1])
    require(ec_on(A840, img1) and ec_on(A840, img2), "transport lands on E")
    T = (Fraction(-840), Fraction(0))
    Q = ec_add(A840, img1, T)
    require(Q == (Fraction(1960), Fraction(78400)), "Q from transport")
    R = img2
    require(R == (Fraction(1176), Fraction(28224)), "R from transport")
    require(ec_mul(A840, 2, Q) == (Fraction(841), Fraction(-1189)), "2Q")
    require(ec_mul(A840, 2, R) == (Fraction(1369), Fraction(-39997)), "2R")

    # saturation certificate.  Variables (R,S,W) unsquared; (r,s,w) squared.
    n6 = 6  # R,S,W,A,B,C
    Rv, Sv, Wv, Av, Bv, Cv = (Poly.var(n6, i) for i in range(6))
    F6 = (2 * Rv ** 2 * Sv ** 2 - (1 + Wv ** 2) * (Rv ** 2 + Sv ** 2)
          + 2 * Wv ** 2)
    lead = 2 * Rv ** 2 - Wv ** 2 - 1
    const = 2 * Wv ** 2 - (1 + Wv ** 2) * Rv ** 2
    require((F6 - (lead * Sv ** 2 + const)).is_zero(), "F as poly in S")
    g1p = Av ** 2 - Rv ** 2 * Sv ** 2 - Wv ** 2
    g2p = Bv ** 2 - Rv ** 2 * Wv ** 2 - Sv ** 2
    g3p = Cv ** 2 - Rv ** 2 - Sv ** 2 * Wv ** 2
    conic = 2 * Av ** 2 - Bv ** 2 - Cv ** 2
    require((conic - (2 * g1p - g2p - g3p + F6)).is_zero(),
            "2A^2=B^2+C^2 lies in the ideal")
    # irreducibility premises
    comb = (Wv ** 2 + 1) * lead + 2 * const
    require((comb + (Wv ** 2 - 1) ** 2).is_zero(),
            "leading/constant Bezout combination")
    require(not lead.subst(2, 1).is_zero(), "lead nonzero at W=1")
    require(lead.eval_at((0, 0, 0, 0, 0, 0)) == -1
            and (4 * Rv).eval_at((0, 0, 0, 0, 0, 0)) == 0
            and (2 * Wv).eval_at((0, 0, 0, 0, 0, 0)) == 0,
            "squarefreeness of the leading coefficient")
    num_ratio = (1 + Wv ** 2) * Rv ** 2 - 2 * Wv ** 2
    require((2 * num_ratio - (Wv ** 2 + 1) * lead - (Wv ** 2 - 1) ** 2)
            .is_zero(), "odd-order remainder identity")

    # squared-coordinate chart (r,s) with w eliminated: on F=0,
    #   w = (r+s-2rs)/(2-r-s), and the three radicands become
    #   p_A = (r+s)(1-rs)/(2-r-s),  p_B = N_B/(2-r-s),  p_C = N_C/(2-r-s)
    n2 = 2
    r_, s_ = Poly.var(n2, 0), Poly.var(n2, 1)
    w_num = r_ + s_ - 2 * r_ * s_
    w_den = 2 - r_ - s_
    f2_cleared = (2 * r_ * s_) * w_den - (w_den + w_num) * (r_ + s_) \
        + 2 * w_num
    require(f2_cleared.is_zero(), "surface parametrization identity")
    N_A = (r_ + s_) * (1 - r_ * s_)
    N_B = r_ ** 2 - 2 * r_ ** 2 * s_ + 2 * s_ - s_ ** 2
    N_C = s_ ** 2 - 2 * r_ * s_ ** 2 + 2 * r_ - r_ ** 2
    require(((w_num + r_ * s_ * w_den) - N_A).is_zero(), "p_A numerator")
    require(((r_ * w_num + s_ * w_den) - N_B).is_zero(), "p_B numerator")
    require(((s_ * w_num + r_ * w_den) - N_C).is_zero(), "p_C numerator")
    require((N_C - 2 * N_A + N_B).is_zero(),
            "p_C = 2 p_A on the p_B branch (N_C - 2N_A = -N_B)")
    # N_B irreducible: as a quadratic in s its discriminant is
    # 4(r^4 - r^2 + 1), and r^4 - r^2 + 1 is not a square in Q[r]: a square
    # root would be +-(r^2 + a r + b); matching r^3 forces a = 0, matching
    # r^2 then forces b = -1/2, and the constant term b^2 = 1/4 != 1.
    rr = Poly.var(1, 0)
    a_forced, b_forced = Fraction(0), Fraction(-1, 2)
    require(2 * a_forced == 0 and a_forced ** 2 + 2 * b_forced == -1
            and b_forced ** 2 != 1, "discriminant nonsquare forcing chain")
    require(not ((rr ** 4 - rr ** 2 + 1)
                 - (rr ** 2 + a_forced * rr + b_forced) ** 2).is_zero(),
            "forced candidate fails, so no square root exists")
    # generic nonvanishing across branches
    require(N_B.subst(1, -1 * r_).equals(2 * r_ ** 3 - 2 * r_),
            "N_B on r+s=0")
    num_B_rs1 = Poly.var(1, 0) ** 4 - 2 * Poly.var(1, 0) ** 3 \
        + 2 * Poly.var(1, 0) - 1
    require((num_B_rs1 - (rr - 1) ** 3 * (rr + 1)).is_zero(),
            "N_B on rs=1 factors as (r-1)^3(r+1)")
    require(N_C.subst(1, -1 * r_).equals(2 * r_ - 2 * r_ ** 3),
            "N_C on r+s=0")
    # 30 saturated factors: none is proportional to F (degrees/monomials)
    factors30 = []
    for expr in ("R+1", "R+S", "R+W", "R-1", "R-S", "R-W", "S+1", "S+W",
                 "S-1", "S-W", "W+1", "W-1"):
        factors30.append(expr)
    factors30 += [
        "R*S+R+S*W-W", "R*S+R-S*W+W", "R*S-R+S*W+W", "R*S-R-S*W-W",
        "R*S+R*W+S-W", "R*S+R*W-S+W", "R*S-R*W+S+W", "R*S-R*W-S-W",
        "R*W+R+S*W-S", "R*W+R-S*W+S", "R*W-R+S*W+S", "R*W-R-S*W-S",
        "R^2*S^2-R^2+2*R*S*W-S^2*W^2+W^2",
        "R^2*S^2-R^2-2*R*S*W-S^2*W^2+W^2",
        "R^2*S^2-R^2*W^2+2*R*S*W-S^2+W^2",
        "R^2*S^2-R^2*W^2-2*R*S*W-S^2+W^2",
        "R^2*W^2-R^2+2*R*S*W-S^2*W^2+S^2",
        "R^2*W^2-R^2-2*R*S*W-S^2*W^2+S^2",
    ]
    require(len(factors30) == 30 and len(set(factors30)) == 30,
            "30 distinct normalized factors")

    def parse_factor(expr: str) -> Poly:
        out = Poly.const(n6, 0)
        for term in expr.replace("-", "+-").split("+"):
            if not term:
                continue
            coef = Fraction(1)
            mono = Poly.const(n6, 1)
            if term.startswith("-"):
                coef = -coef
                term = term[1:]
            for atom in term.split("*"):
                if not atom:
                    continue
                if "^" in atom:
                    sym, e = atom.split("^")
                    e = int(e)
                else:
                    sym, e = atom, 1
                if sym.isdigit():
                    coef *= Fraction(int(sym)) ** e
                else:
                    idx = {"R": 0, "S": 1, "W": 2}[sym]
                    mono = mono * Poly.var(n6, idx, e)
            out = out + coef * mono
        return out

    for expr in factors30:
        gpoly = parse_factor(expr)
        # F is irreducible of degree 4; a factor vanishing on {F=0} would be
        # divisible by F, hence proportional to it.  Rule that out exactly.
        proportional = False
        for kmono, coef in F6.c.items():
            if kmono in gpoly.c:
                ratio = gpoly.c[kmono] / coef
                proportional = (gpoly - ratio * F6).is_zero()
                break
        require(not proportional, f"factor {expr} proportional to F")

    # S5 monodromy certificate at the cone point (A,B,C) = (5,1,7)
    require(2 * 5 ** 2 == 1 ** 2 + 7 ** 2, "cone membership")
    n4 = 4  # r, a, b, c
    rq, aq, bq, cq = (Poly.var(n4, i) for i in range(4))
    quintic_gen = (cq * (1 - rq ** 2) ** 2 - (bq - aq * rq) * (aq - bq * rq)
                   - rq * (1 - rq ** 2) ** 2)
    # inverse reconstruction identities: with s=(b-ar)/(1-r^2),
    # w=(a-br)/(1-r^2):  rs+w = a  and  rw+s = b  identically, and
    # (sw+r) - c = -Q(r)/(1-r^2)^2.
    s_num, w_num2 = bq - aq * rq, aq - bq * rq
    one_r2 = 1 - rq ** 2
    require((rq * s_num + w_num2 - aq * one_r2).is_zero(), "inverse a")
    require((rq * w_num2 + s_num - bq * one_r2).is_zero(), "inverse b")
    require(((s_num * w_num2 + rq * one_r2 ** 2) - cq * one_r2 ** 2
             + quintic_gen).is_zero(), "inverse c vs quintic")
    spec = {1: 25, 2: 1, 3: 49}
    qspec = quintic_gen
    for i, val in spec.items():
        qspec = qspec.subst(i, val)
    coeffs = [0] * 6
    for k, coef in qspec.c.items():
        require(coef.denominator == 1, "integral quintic")
        coeffs[k[0]] = int(coef)
    require(coeffs == [24, 625, -123, 2, 49, -1], f"quintic coeffs {coeffs}")
    require(factor_degree_pattern(coeffs, 7) == [5], "irreducible mod 7")
    require(factor_degree_pattern(coeffs, 29) == [2, 1, 1, 1],
            "degree pattern [2,1,1,1] mod 29")
    disc = quintic_discriminant(coeffs)
    require(disc == -24364389070416096000, f"quintic discriminant {disc}")
    emit("family3: interaction equation, MW transport, saturation premises "
         "and S5 monodromy (mod 7 irreducible, mod 29 [2,1,1,1], "
         f"disc {disc}) verified")
    return {
        "interaction_equation": "eight sums agree iff x1+x2=2x0",
        "mw_lock": {"minimal_model": "y^2=x^3-44100x",
                    "generators": [[-84, -1764], [294, 3528]],
                    "Q": [1960, 78400], "R": [1176, 28224],
                    "two_Q": [841, -1189], "two_R": [1369, -39997]},
        "saturation": {"conic_in_ideal": True,
                       "irreducibility_premises": True,
                       "branch_divisors": True,
                       "saturated_factors": 30},
        "s5_monodromy": {"quintic": coeffs, "mod7": [5],
                         "mod29": [2, 1, 1, 1],
                         "discriminant": disc,
                         "degrees": {"squared_quotient": 5,
                                     "signed_cover": 40}},
    }


# --------------------------------------------------------------------------
# family 4 -- Section 5.2: the x0 = 841 fibre
# --------------------------------------------------------------------------

def family4(emit) -> dict:
    A_, B_ = 841 ** 2, 1681 ** 2
    L_ = A_ * B_
    require((A_, B_, L_) == (707281, 2825761, 1998607065841), "A, B, L")
    # the genus-two curve C: w^2 = (1-t^2)(A-t^2)(B-t^2); its complementary
    # bielliptic quotient is v^2 = (u-A)(u-B)(u-L) via u = L/t^2, v = Lw/t^3
    n = 2
    t, w = Poly.var(n, 0), Poly.var(n, 1)
    sextic = (1 - t ** 2) * (A_ - t ** 2) * (B_ - t ** 2)
    lhs = (L_ * w) ** 2
    rhs = ((L_ - A_ * t ** 2) * (L_ - B_ * t ** 2) * (L_ - L_ * t ** 2))
    require((lhs.reduce_square(1, sextic) - L_ * L_ * sextic).is_zero(),
            "v^2 clears to L^2 w^2")
    require((rhs - L_ * L_ * sextic).is_zero(), "quotient map identity")
    # torsion x-values and the pulled-back t-list
    quot_roots = sorted((A_, B_, L_))
    tlist = sorted({0} | {s * math.isqrt(L_ // u) for u in quot_roots
                          for s in (1, -1)})
    require(all(is_square(L_ // u) for u in quot_roots), "L/u squares")
    require(tlist == [-1681, -841, -1, 0, 1, 841, 1681], "pulled-back t-list")
    # leading coefficient of the even model is -1: not a rational square
    require(rational_sqrt(Fraction(-1)) is None, "-1 nonsquare")
    # positivity window: 841 +- t > 840 iff |t| < 1
    admissible = [tv for tv in tlist if abs(tv) < 1]
    require(admissible == [0], "positive window leaves only t=0")

    # expansion of (u-A)(u-B)(u-L) matches the frozen curve line
    e1 = A_ + B_ + L_
    e2 = A_ * B_ + A_ * L_ + B_ * L_
    e3 = A_ * B_ * L_
    require(e1 == 1998610598883 and e2 == 7061164703720084163
            and e3 == 3994430203629571309037281, "cubic coefficients")

    # frozen transcript + machine-readable certificate
    tr = parse_transcript(load_frozen(
        "centre841_bielliptic_fibre_magma_v2_29_8.txt").decode("utf-8"))
    require(t_value(tr, "MAGMA_VERSION") == "2 29 8", "magma version")
    require(t_value(tr, "RANK_BOUNDS") == "0 0" and t_value(tr, "RANK") == "0"
            and t_value(tr, "RANK_PROVED") == "true", "rank 0 proved")
    require(t_value(tr, "TORSION_ORDER") == "4"
            and parse_int_list(t_value(tr, "TORSION_INVARIANTS")) == [2, 2],
            "torsion (Z/2)^2")
    require(parse_int_list(t_value(tr, "NONZERO_TORSION_X"))
            == [707281, 2825761, 1998607065841], "torsion x-list")
    require(f"x^3 - {e1}*x^2 + {e2}*x - {e3}" in t_value(tr, "CURVE"),
            "curve line matches the expanded cubic")
    require(t_value(tr, "ASSERTIONS") == "PASS"
            and t_value(tr, "STATUS") == "PASS_INDEPENDENT_MAGMA_REPLAY",
            "transcript status")
    cert = json.loads(load_frozen(
        "centre841_magma_certificate.json").decode("utf-8"))
    require(cert["output"]["rank_bounds"] == [0, 0]
            and cert["output"]["rank"] == 0
            and cert["output"]["rank_proved"] is True
            and cert["output"]["torsion_invariants"] == [2, 2]
            and cert["output"]["nonzero_torsion_x"]
            == [707281, 2825761, 1998607065841], "certificate output")
    require(cert["transcript_artifact"]["sha256"]
            == FROZEN_FILES["centre841_bielliptic_fibre_magma_v2_29_8.txt"][0],
            "certificate pins the shipped transcript")
    require(cert["input_artifact"]["sha256"]
            == FROZEN_FILES["centre841_bielliptic_fibre.m"][0],
            "certificate pins the shipped calculator input")
    require(all(v is False for v in cert["boundary"].values()),
            "certificate non-claim boundary flags")
    pari = parse_transcript(load_frozen(
        "centre841_first_quotient_pari_v2_17_4.txt").decode("utf-8"))
    require(t_value(pari, "PARI_VERSION") == "[2, 17, 4]",
            "PARI version")
    require(t_value(pari, "CURVE_A_INVARIANTS")
            == "[0,3533043,0,1998610598883,1998607065841]",
            "first quotient coefficients")
    require(t_value(pari, "RANK_RESULT").startswith("[3, 3, 0,"),
            "first quotient rank bounds 3,3")
    require(t_value(pari, "TORSION_RESULT").startswith("[4, [2, 2],"),
            "first quotient torsion")
    require(t_value(pari, "STATUS") == "PASS_CORROBORATION_ONLY",
            "PARI corroboration status")
    emit("family4: x0=841 fibre algebra exact; t-list {0,+-1,+-841,+-1681}; "
         "rank-0 transcript and contextual PARI rank-3 record verified")
    return {
        "curve": "w^2=(1-t^2)(841^2-t^2)(1681^2-t^2)",
        "quotient": "v^2=(u-841^2)(u-1681^2)(u-841^2*1681^2)",
        "quotient_identity": True,
        "t_list": tlist,
        "admissible_t": admissible,
        "transcript": {"rank": 0, "rank_proved": True,
                       "torsion_invariants": [2, 2]},
        "contextual_first_quotient": {
            "rank_bounds": [3, 3],
            "engine": "PARI/GP 2.17.4",
            "load_bearing": False,
        },
    }


# --------------------------------------------------------------------------
# family 4b -- Section 5.3: the fixed Bremner shadow
# --------------------------------------------------------------------------

def family4b_bremner_shadow(emit) -> dict:
    B = ((88, -153, 65), (-23, 0, 23), (-65, 153, -88))
    lines = (
        B[0], B[1], B[2],
        (B[0][0], B[1][0], B[2][0]),
        (B[0][1], B[1][1], B[2][1]),
        (B[0][2], B[1][2], B[2][2]),
        (B[0][0], B[1][1], B[2][2]),
        (B[0][2], B[1][1], B[2][0]),
    )
    require(all(sum(line) == 0 for line in lines), "B is zero-sum magic")
    require(sorted(abs(v) for row in B for v in row if v)
            == [23, 23, 65, 65, 88, 88, 153, 153],
            "Bremner-shadow coefficients")

    # If 1+-23t and 1+-65t are squares, their two products give
    # Y^2=(1-23^2 t^2)(1-65^2 t^2).  Under x=1/t^2, y=Y/t^3 this is E.
    n = 3
    tv, Yv, xv = (Poly.var(n, i) for i in range(n))
    cover_rhs = (1 - 23 ** 2 * tv ** 2) * (1 - 65 ** 2 * tv ** 2)
    curve_poly = xv * (xv - 529) * (xv - 4225)

    def reciprocal_square_cubic_pullback(poly: Poly) -> Poly:
        """Return t^6*f(1/t^2) by transforming the terms of a cubic f(x)."""
        require(poly.deg_in(2) == 3, "shadow quotient is a cubic in x")
        out = Poly.const(n, 0)
        for powers, coefficient in poly.c.items():
            require(powers[0] == powers[1] == 0 and powers[2] <= 3,
                    "shadow cubic uses x only")
            out += coefficient * tv ** (2 * (3 - powers[2]))
        return out

    curve_pullback_cleared = reciprocal_square_cubic_pullback(curve_poly)
    require((curve_pullback_cleared - cover_rhs).is_zero(),
            "shadow quotient map after denominator clearing")
    require((Yv ** 2 - curve_pullback_cleared)
            .reduce_square(1, cover_rhs).is_zero(),
            "shadow double-cover maps to the elliptic curve")

    raw = load_frozen(
        "bremner_shadow_pair_quotients_pari_v2_17_4.txt"
    ).decode("utf-8")
    rows = [line.split("|") for line in raw.splitlines() if "|" in line]
    one = {}
    for row in rows:
        one.setdefault(row[0], []).append(row[1:])
    require(raw.startswith("BREMNER_SHADOW_PARI_BEGIN\n")
            and raw.rstrip().endswith("BREMNER_SHADOW_PARI_DONE"),
            "shadow transcript sentinels")
    require(one["PARI_VERSION"] == [["[2, 17, 4]"]], "shadow PARI version")
    curve_coefficients = {
        powers[2]: coefficient for powers, coefficient in curve_poly.c.items()
    }
    require(curve_coefficients.get(3) == 1, "shadow curve is monic cubic")
    original_ainvs = [[
        "0", fstr(curve_coefficients.get(2, Fraction(0))), "0",
        fstr(curve_coefficients.get(1, Fraction(0))),
        fstr(curve_coefficients.get(0, Fraction(0))),
    ]]
    require(one["SELECTED_ORIGINAL_AINVS"] == original_ainvs,
            "shadow original model")
    require(one["SELECTED_MIN_AINVS"] == [["1", "0", "0", "-331155", "-69042600"]],
            "shadow minimal model")
    require(one["SELECTED_CONDUCTOR"] == [["345345"]]
            and one["SELECTED_CREMONA"] == [["345345r4"]],
            "shadow catalogue identity")
    require(one["SELECTED_RANK"] == [["[0, 0, 0, []]"]],
            "shadow unconditional rank interval")
    require(one["SELECTED_TORSION"][0][0].startswith("[4, [2, 2],"),
            "shadow transcript torsion")

    def count_points(prime: int) -> int:
        total = 1
        for xval in range(prime):
            rhs = int(curve_poly.eval_at((0, 0, xval)))
            total += 1 + legendre(rhs, prime)
        return total

    counts = {17: count_points(17), 41: count_points(41)}
    require(counts == {17: 16, 41: 40}, "shadow finite-field counts")
    require(one["SELECTED_CARD"] == [["17", "16"], ["41", "40"]],
            "shadow transcript finite-field counts")
    require(math.gcd(*counts.values()) == 8, "shadow torsion order bound")

    roots = (0, 529, 4225)
    halving = {}
    for root in roots:
        diffs = [Fraction(root - other) for other in roots if other != root]
        sq = [rational_sqrt(value) is not None for value in diffs]
        halving[str(root)] = sq
        require(not all(sq), f"2-torsion point at x={root} is not halved")

    candidates = (Fraction(1, 23), Fraction(-1, 23),
                  Fraction(1, 65), Fraction(-1, 65))
    rejected = {}
    for parameter in candidates:
        forms = [1 + sign * a * parameter
                 for a in (23, 65) for sign in (1, -1)]
        require(Fraction(2) in forms, "candidate has a form equal to 2")
        require(any(rational_sqrt(value) is None for value in forms),
                "candidate rejected by original square conditions")
        rejected[fstr(parameter)] = [fstr(value) for value in forms]
    zero_forms = [Fraction(1) + sign * a * Fraction(0)
                  for a in (23, 65, 88, 153) for sign in (1, -1)]
    require(zero_forms == [Fraction(1)] * 8
            and all(rational_sqrt(value) is not None for value in zero_forms),
            "t=0 survives all eight original square conditions")

    emit("family4b: fixed Bremner shadow closed -- rank 0, torsion (Z/2)^2, "
         "and every nonzero pulled-back parameter rejected exactly")
    return {
        "coefficient_matrix": [list(row) for row in B],
        "curve": "y^2=x(x-529)(x-4225)",
        "quotient_map": "x=1/t^2, y=Y/t^3",
        "cremona_label": "345345r4",
        "rank_bounds": [0, 0],
        "finite_field_counts": {str(p): value for p, value in counts.items()},
        "torsion_invariants": [2, 2],
        "halving_tests": halving,
        "rejected_nonzero_parameters": rejected,
        "admissible_parameter": "0",
    }


# --------------------------------------------------------------------------
# family 5 -- Section 5.4: the half-class stop
# --------------------------------------------------------------------------

def kummer_delta(P) -> tuple:
    """Ordered squarefree triple (sc(x+840), sc(x), sc(x-840)); at a
    two-torsion point the vanishing slot is replaced by the product of the
    other two (the standard complete two-descent convention)."""
    x = Fraction(P[0])
    vals = [x + D, x, x - D]
    out = []
    for i, v in enumerate(vals):
        if v == 0:
            others = [vals[j] for j in range(3) if j != i]
            out.append(squarefree_signed(others[0] * others[1]))
        else:
            out.append(squarefree_signed(v))
    return tuple(out)


def family5(emit) -> dict:
    Q = (Fraction(1960), Fraction(78400))
    R = (Fraction(1176), Fraction(28224))
    require(ec_on(A840, Q) and ec_on(A840, R), "Q, R on curve")
    H = ec_add(A840, Q, ec_mul(A840, 2, R))
    require(H == (Fraction(331240, 9), Fraction(-190590400, 27)), "H = Q+2R")
    dQ, dR, dH = kummer_delta(Q), kummer_delta(R), kummer_delta(H)
    require(dQ == (7, 10, 70), f"delta(Q) {dQ}")
    require(dR == (14, 6, 21), f"delta(R) {dR}")
    require(dH == dQ, "delta(H) = delta(Q)")
    H2 = ec_mul(A840, 2, H)
    require(H2[0] == Fraction(490152611881, 53187849), "x(2H)")
    roots = [rational_sqrt(H2[0] - D), rational_sqrt(H2[0]),
             rational_sqrt(H2[0] + D)]
    require(roots == [Fraction(667439, 7293), Fraction(700109, 7293),
                      Fraction(731321, 7293)], "2H square progression")
    torsion_images = sorted(
        {kummer_delta((Fraction(-840), Fraction(0))),
         kummer_delta((Fraction(0), Fraction(0))),
         kummer_delta((Fraction(840), Fraction(0))),
         (1, 1, 1)})
    require(torsion_images == [(1, 1, 1), (2, -210, -105), (105, 210, 2),
                               (210, -1, -210)], "torsion Kummer images")
    prodQR = tuple(squarefree_signed(Fraction(a * b))
                   for a, b in zip(dQ, dR))
    require(prodQR == (2, 15, 30), "delta(Q)*delta(R)")
    for img in (dQ, dR, prodQR):
        require(img not in torsion_images, "rank-two structure")

    family_rows = []
    x2Q = ec_mul(A840, 2, Q)[0]
    for nlev in (1, 2, 3):
        Hn = ec_add(A840, Q, ec_mul(A840, 2 ** nlev, R))
        dHn = kummer_delta(Hn)
        x2Hn = ec_mul(A840, 2, Hn)[0]
        require(dHn == dQ, f"delta(Q+2^{nlev}R) = delta(Q)")
        require(x2Hn != x2Q, f"x(2(Q+2^{nlev}R)) != x(2Q)")
        true_triple_ok = (x2Q + x2Q == 2 * x2Q)
        false_triple_ok = (x2Q + x2Hn == 2 * x2Q)
        require(true_triple_ok and not false_triple_ok,
                "triple interaction separation")
        family_rows.append({"n": nlev, "x_2H": fstr(x2Hn)})
    emit("family5: half-class countercertificate exact -- delta(Q+2^nR) = "
         "delta(Q) = (7,10,70) while the doubled centres differ (n=1,2,3)")
    return {
        "delta_Q": list(dQ), "delta_R": list(dR),
        "H": [fstr(H[0]), fstr(H[1])],
        "x_2H": fstr(H2[0]),
        "roots_2H": [fstr(r) for r in roots],
        "torsion_images": [list(t) for t in torsion_images],
        "family_levels": family_rows,
    }


# --------------------------------------------------------------------------
# family 6 -- Section 6: the support law
# --------------------------------------------------------------------------

def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    r = pow(a, (p - 1) // 2, p)
    return 1 if r == 1 else -1


def family6(emit) -> dict:
    # abstract torus identity: per index, z = u/v with u v = 2d and
    # u^2 + v^2 = 4 s^2 gives (z + 1/z) * 2d = 4 s^2, by the exact cofactor
    # identity  2d(u^2+v^2) - 4 s^2 u v = -(u^2+v^2)(uv-2d) + uv(u^2+v^2-4s^2).
    # Summing with weights (1,1,-2) turns (L.1) into s1^2+s2^2 = 2 s0^2.
    n4 = 4  # u, v, d, s
    uv_, vv_, dv_, sv_ = (Poly.var(n4, i) for i in range(4))
    con1 = uv_ * vv_ - 2 * dv_
    con2 = uv_ ** 2 + vv_ ** 2 - 4 * sv_ ** 2
    lhs4 = 2 * dv_ * (uv_ ** 2 + vv_ ** 2) - 4 * sv_ ** 2 * uv_ * vv_
    require((lhs4 - (-(uv_ ** 2 + vv_ ** 2) * con1 + uv_ * vv_ * con2))
            .is_zero(), "abstract torus clearing identity")

    # surface-coordinate torus identity: with z0=W/(RS), z1=RW/S, z2=SW/R,
    # (z1 + 1/z1 + z2 + 1/z2 - 2 z0 - 2/z0) * RSW = -F, and the normalized
    # unit equation U := (z0z1 + z0/z1 + z0z2 + z0/z2)/2 - z0^2 satisfies
    # (U - 1) * 2R^2S^2 = the same cleared polynomial, so U = 1 on F = 0.
    n3 = 3
    Rv, Sv, Wv = (Poly.var(n3, i) for i in range(3))
    F3 = (2 * Rv ** 2 * Sv ** 2 - (1 + Wv ** 2) * (Rv ** 2 + Sv ** 2)
          + 2 * Wv ** 2)
    cleared = (Rv ** 2 * Wv ** 2 + Sv ** 2 + Sv ** 2 * Wv ** 2 + Rv ** 2
               - 2 * Wv ** 2 - 2 * Rv ** 2 * Sv ** 2)
    require((cleared + F3).is_zero(), "torus identity clears to -F")
    U_minus_1_cleared = (Wv ** 2 * Rv ** 2 + Sv ** 2 + Wv ** 2 * Sv ** 2
                         + Rv ** 2 - 2 * Wv ** 2 - 2 * Rv ** 2 * Sv ** 2)
    require((U_minus_1_cleared + F3).is_zero(),
            "unit equation (U-1)*2R^2S^2 = -F")

    # nondegeneracy consequence table (Sec. 6.1): the fourteen proper
    # subsums of the five-term unit equation, with the load-bearing pair
    # collapses verified as exact polynomial identities in the squared
    # chart (r,s,w), where F reads f2 = 2rs - (1+w)(r+s) + 2w.
    r_, s_, w_ = (Poly.var(n3, i) for i in range(3))
    f2 = 2 * r_ * s_ - (1 + w_) * (r_ + s_) + 2 * w_
    require(f2.subst(1, 2 - r_).equals(-2 * (r_ - 1) ** 2),
            "pair {0,2} collapse: r=s=1")
    require(f2.subst(1, 2 * w_ - r_).equals(-2 * (r_ - w_) ** 2),
            "pair {1,3} collapse: r=s=w")
    # r = 2w/(1+w) cleared by (1+w): (1+w) f2 -> -s(w-1)^2
    expr = (2 * (2 * w_) * s_ - (1 + w_) * ((2 * w_) + (1 + w_) * s_)
            + 2 * w_ * (1 + w_))
    require(expr.equals(-1 * s_ * (w_ - 1) ** 2),
            "pair {0,3} collapse: r=w=1")
    expr_sym = (2 * r_ * (2 * w_) - (1 + w_) * ((1 + w_) * r_ + (2 * w_))
                + 2 * w_ * (1 + w_))
    require(expr_sym.equals(-1 * r_ * (w_ - 1) ** 2),
            "pair {1,2} collapse: s=w=1")
    consequences = {
        "0": "z1=2z0 <=> r=2", "1": "1/z1=2z0 <=> s=2w",
        "2": "z2=2z0 <=> s=2", "3": "1/z2=2z0 <=> r=2w",
        "01": "B^2=2W^2 (2 not a rational square)",
        "23": "C^2=2W^2 (2 not a rational square)",
        "02": "r=s=1", "13": "r=s=w", "03": "r=w=1", "12": "s=w=1",
        "012": "2s=1", "013": "w=2r", "023": "2r=1", "123": "w=2s",
    }
    require(len(consequences) == 14, "14 proper subsums")
    require(rational_sqrt(Fraction(2)) is None, "2 is not a rational square")
    # the z-ratio identities behind the singleton/pair/triple rows, cleared:
    #   z1/z0 = R^2, z2/z0 = S^2, z1 z2 = W^2, z0 z1 = W^2/S^2,
    #   z0 z2 = W^2/R^2, z0/z1 = 1/R^2, z0/z2 = 1/S^2
    z0n, z0d = Wv, Rv * Sv
    z1n, z1d = Rv * Wv, Sv
    z2n, z2d = Sv * Wv, Rv
    require((z1n * z0d - Rv ** 2 * (z1d * z0n)).is_zero(), "z1/z0 = R^2")
    require((z2n * z0d - Sv ** 2 * (z2d * z0n)).is_zero(), "z2/z0 = S^2")
    require((z1n * z2n - Wv ** 2 * (z1d * z2d)).is_zero(), "z1 z2 = W^2")
    require((z0n * z1n * Sv ** 2 - Wv ** 2 * (z0d * z1d)).is_zero(),
            "z0 z1 = W^2/S^2")
    require((z0n * z2n * Rv ** 2 - Wv ** 2 * (z0d * z2d)).is_zero(),
            "z0 z2 = W^2/R^2")
    # nondegeneracy-repair identities now proved in the paper (Sec. 6.1):
    # mixed cross terms collapse via the exact elimination
    #   from  a*b + k = 2*b*c  and  k*c + a*b*c = 2*k*a :
    #   substituting a = (2bc-k)/b and clearing b gives 2*(b*c - k)^2 = 0,
    # and pure cross terms collapse via x+y=2, xy=1 => (t-1)^2 = 0.
    b_, c_, k_ = (Poly.var(3, i) for i in range(3))
    mixed = (k_ * b_ * c_ + (2 * b_ * c_ - k_) * b_ * c_
             - 2 * k_ * (2 * b_ * c_ - k_))
    require(mixed.equals(2 * (b_ * c_ - k_) ** 2),
            "mixed-cross collapse identity")
    t_ = Poly.var(1, 0)
    require((t_ * t_ - 2 * t_ + 1).equals((t_ - 1) ** 2),
            "pure-cross collapse identity")

    # pair {0,1} cleared: (z1 + 1/z1 - 2 z0) * RSW = R^2W^2 + S^2 - 2W^2,
    # the radicand identity B^2 - 2W^2; symmetrically for {2,3} and C.
    pair01 = Rv ** 2 * Wv ** 2 + Sv ** 2 - 2 * Wv ** 2
    pair23 = Sv ** 2 * Wv ** 2 + Rv ** 2 - 2 * Wv ** 2
    b2 = Rv ** 2 * Wv ** 2 + Sv ** 2
    c2 = Sv ** 2 * Wv ** 2 + Rv ** 2
    require((pair01 - (b2 - 2 * Wv ** 2)).is_zero(), "pair {0,1} = B^2-2W^2")
    require((pair23 - (c2 - 2 * Wv ** 2)).is_zero(), "pair {2,3} = C^2-2W^2")

    # endpoint pigeonhole replay: e = 1..12, all (a0,a1,a2) in [0,e]^3
    checked = 0
    for e in range(1, 13):
        for a0 in range(e + 1):
            for a1 in range(e + 1):
                for a2 in range(e + 1):
                    nus = [2 * a0 - e, 2 * a1 - e, 2 * a2 - e]
                    endpoints = sum(1 for a in (a0, a1, a2) if a in (0, e))
                    mx = max(abs(v) for v in nus)
                    tied = sum(1 for v in nus if abs(v) == mx) >= 2
                    if endpoints >= 1 and tied:
                        require(endpoints >= 2,
                                f"pigeonhole fails at e={e}")
                    checked += 1
    require(checked == sum((e + 1) ** 3 for e in range(1, 13)),
            "pigeonhole coverage")

    # mod-8 endpoint table from quadratic residues, with witness primes
    table = {}
    witnesses = {1: [17, 41, 73], 3: [3, 11, 19], 5: [5, 13, 29],
                 7: [7, 23, 31]}
    expected = {1: ["01", "02", "12"], 3: [], 5: ["12"], 7: ["01", "02"]}
    for res, primes in sorted(witnesses.items()):
        pairs_per_prime = []
        for p in primes:
            require(p % 8 == res % 8 or (res == 3 and p == 3),
                    "witness residue")
            minus1 = legendre(-1, p)
            two = legendre(2, p)
            pairs = []
            if two == 1:
                pairs += ["01", "02"]
            if minus1 == 1:
                pairs.append("12")
            pairs_per_prime.append(sorted(pairs))
        require(all(pp == pairs_per_prime[0] for pp in pairs_per_prime),
                f"endpoint table residue {res}")
        require(pairs_per_prime[0] == expected[res],
                f"endpoint table row {res}")
        table[str(res)] = expected[res]

    # {2,3} exclusion replay: for e2 = v_2(2d) >= 4, e3 >= 1 the candidate
    # values are z in {2^(+-(e2-2)) 3^(+-e3)}; f(z) = z + 1/z takes at most
    # two values, is strictly decreasing on (0,1), and the mean equation
    # forces all three z equal.
    cases = 0
    for e2 in range(4, 10):
        for e3 in range(1, 6):
            zs = sorted({Fraction(2) ** s2 * Fraction(3) ** s3
                         for s2 in (e2 - 2, -(e2 - 2))
                         for s3 in (e3, -e3)})
            small = [zv for zv in zs if zv < 1]
            fvals = sorted({zv + 1 / zv for zv in small})
            require(len(fvals) == 2, "two f-values")
            xs = sorted(small)
            require(xs[0] < xs[1]
                    and (xs[0] + 1 / xs[0]) > (xs[1] + 1 / xs[1]),
                    "f strictly decreasing on the candidates")
            for z0v in small:
                for z1v in small:
                    for z2v in small:
                        if (z1v + 1 / z1v) + (z2v + 1 / z2v) \
                                == 2 * (z0v + 1 / z0v):
                            require(z0v == z1v == z2v,
                                    "mean equation forces equality")
                        cases += 1
    emit("family6: torus identity (abstract and on-surface), 14-subsum "
         "table, endpoint pigeonhole (e<=12), mod-8 table and {2,3} "
         "exclusion replayed")
    return {
        "torus_identity_on_surface": "(L.1)*RSW = -F",
        "unit_equation": "U = 1 + z0*T/2",
        "nondegeneracy_consequences": consequences,
        "endpoint_table_mod8": table,
        "exclusion_23_cases": cases,
    }


# --------------------------------------------------------------------------
# family 7 -- Section 7: three-prime exclusion
# --------------------------------------------------------------------------

def family7(emit) -> dict:
    n = 4  # x, Y, Z, W
    xv, Yv, Zv, Wv = (Poly.var(n, i) for i in range(4))
    # hypotenuse identities for the endpoint types
    require(((2 * xv) ** 2 + (xv ** 2 - 1) ** 2 - (xv ** 2 + 1) ** 2)
            .is_zero(), "type A legs")
    require((4 * Yv ** 2 + (Yv ** 2 - 1) ** 2 - (Yv ** 2 + 1) ** 2)
            .is_zero(), "type B legs (cleared by 4)")
    # pair eliminations
    ab = (Yv * (Yv ** 2 - 1) - 4 * xv * (xv ** 2 - 1)
          - (Yv * (Yv ** 2 - 1 - 4 * xv * Zv)
             + 4 * xv * (Yv * Zv - (xv ** 2 - 1))))
    require(ab.is_zero(), "AB elimination identity")
    ac = (Zv * (Zv ** 2 - 1) - 4 * xv * (xv ** 2 - 1)
          - (Zv * (Zv ** 2 - 1 - 4 * xv * Yv)
             + 4 * xv * (Yv * Zv - (xv ** 2 - 1))))
    require(ac.is_zero(), "AC elimination identity")
    require((((Yv ** 2 - 1 - 4 * xv * Zv) - (Zv ** 2 - 1 - 4 * xv * Yv))
             - (Yv - Zv) * (Yv + Zv + 4 * xv)).is_zero(), "BC difference")
    # three-block proposition (2X convention)
    Xv = Poly.var(n, 0)  # reuse slot as X
    require((((Yv ** 2 - 1 - 2 * Xv * Zv) - (Zv ** 2 - 1 - 2 * Xv * Yv))
             - (Yv - Zv) * (Yv + Zv + 2 * Xv)).is_zero(),
            "three-block collapse")
    # Y(Y-2X) = 1 has no admissible solution: positive integers force Y=1
    sols = [(Y, X) for Y in range(1, 50) for X in range(1, 50)
            if Y * (Y - 2 * X) == 1]
    require(sols == [], "Y(Y-2X)=1 has no positive solution")
    # the two cubic factorizations behind the W = 2x-1 forcing
    f = lambda t: t * (t ** 2 - 1)  # noqa: E731
    require((f(2 * xv) - 4 * f(xv) - 2 * xv * (2 * xv ** 2 + 1)).is_zero(),
            "upper-bound factor")
    require((f(2 * xv - 1) - 4 * f(xv) - 4 * xv * (xv - 2) * (xv - 1))
            .is_zero(), "forced-value factor")
    # window + residue enumeration: x = 2^alpha, W odd in (x, 2x) with
    # W == +-1 mod 2x leaves only W = 2x-1; the cubic then forces x = 2
    for alpha in range(1, 13):
        x = 2 ** alpha
        cands = [W for W in range(x + 1, 2 * x)
                 if W % (2 * x) in (1, 2 * x - 1)]
        require(cands == ([] if x == 1 else [2 * x - 1]), "window residues")
    hits = []
    for npow in range(1, 101):
        x = 2 ** npow
        target = 4 * x * (x ** 2 - 1)
        w0 = icbrt(target)
        for W in range(max(3, w0 - 2), w0 + 4):
            if W * (W ** 2 - 1) == target:
                hits.append((x, W))
    require(hits == [(2, 3)], "cubic diagnostic hits")
    # x=2, W=3: the remaining block (x^2-1)/W = 1 is not a prime power in
    # the support
    require((2 ** 2 - 1) // 3 == 1, "final block equals 1")

    # one-interior branch laws: the nine expansion identities
    n3 = 3  # X, Y, Z
    X3, Y3, Z3 = (Poly.var(n3, i) for i in range(3))
    HA = X3 ** 2 + Y3 ** 2 * Z3 ** 2
    HB = X3 ** 2 * Z3 ** 2 + Y3 ** 2
    HC = X3 ** 2 * Y3 ** 2 + Z3 ** 2
    require((HA + HB - (X3 ** 2 + Y3 ** 2) * (Z3 ** 2 + 1)).is_zero(),
            "p5 sum AB")
    require((HA + HC - (X3 ** 2 + Z3 ** 2) * (Y3 ** 2 + 1)).is_zero(),
            "p5 sum AC")
    require((HB + HC - (X3 ** 2 + 1) * (Y3 ** 2 + Z3 ** 2)).is_zero(),
            "p5 sum BC")
    require((2 * HA - HB - ((2 * X3 ** 2 - Y3 ** 2)
                            + Z3 ** 2 * (2 * Y3 ** 2 - X3 ** 2))).is_zero(),
            "p7 AB")
    require((2 * HA - HC - (X3 ** 2 * (2 - Y3 ** 2)
                            + Z3 ** 2 * (2 * Y3 ** 2 - 1))).is_zero(),
            "p7 AC")
    require((2 * HB - HA - ((2 * Y3 ** 2 - X3 ** 2)
                            + Z3 ** 2 * (2 * X3 ** 2 - Y3 ** 2))).is_zero(),
            "p7 BA")
    require((2 * HB - HC - (Y3 ** 2 * (2 - X3 ** 2)
                            + Z3 ** 2 * (2 * X3 ** 2 - 1))).is_zero(),
            "p7 BC")
    require((2 * HC - HA - (X3 ** 2 * (2 * Y3 ** 2 - 1)
                            + Z3 ** 2 * (2 - Y3 ** 2))).is_zero(),
            "p7 CA")
    require((2 * HC - HB - (Y3 ** 2 * (2 * X3 ** 2 - 1)
                            + Z3 ** 2 * (2 - X3 ** 2))).is_zero(),
            "p7 CB")
    require(vp(1 + 2 ** 10, 5) == 2, "p=5 depth fixture")
    require(vp(2 - 2 ** 22, 7) == 2, "p=7 depth fixture")
    for gamma in range(2, 25):
        for a in range(1, gamma):
            require(2 * min(a, gamma - a) < 2 * gamma, "interior separation")

    # Aebi core crosscheck (AEB26): the six primitive triangles with exactly
    # three area primes used in Section 8
    aebi = [(5, 12, 13), (8, 15, 17), (9, 40, 41), (7, 24, 25),
            (16, 63, 65), (17, 144, 145)]
    areas = []
    thirds = []
    for (u, v, c) in aebi:
        require(u * u + v * v == c * c and math.gcd(u, v) == 1,
                "primitive Pythagorean core")
        area = u * v // 2
        areas.append(area)
        sup = support(area)
        require(len(sup) == 3 and sup[0] == 2 and sup[1] == 3,
                "three area primes {2,3,p}")
        thirds.append(sup[2])
    require(areas == [30, 60, 180, 84, 504, 1224], "Aebi areas")
    require(thirds == [5, 5, 5, 7, 7, 17], "Aebi third primes")
    require(len(set(areas)) == 6, "areas distinct")
    emit("family7: three-block and one-interior identities, the W=2x-1 "
         "forcing (only hit x=2, W=3) and the Aebi crosscheck verified")
    return {
        "three_block_identities": True,
        "w_forcing_hits": [[2, 3]],
        "one_interior_identities": 9,
        "depth_fixtures": {"p5": "v_5(1+2^10)=2", "p7": "v_7(2-2^22)=2"},
        "aebi_cores": [list(t) for t in aebi],
        "aebi_areas": areas,
    }


# --------------------------------------------------------------------------
# family 8 -- Section 8: the four-prime frontier
# --------------------------------------------------------------------------

BALANCED_CORES = [
    (6, (3, 4, 5)), (30, (5, 12, 13)), (60, (8, 15, 17)),
    (180, (9, 40, 41)), (84, (7, 24, 25)), (504, (16, 63, 65)),
    (1224, (17, 144, 145)),
]

FROZEN_SCALED_ROOTS = {
    6: [0, 111, 93750],
    30: [0, 8247435, 144804270],
    60: [0, 29460270, 1448254140],
    180: [0, 18849063610, 95002084820],
    84: [0, 2781750426, 20507812500],
    504: [0, 178747594711, 1055864468750],
    1224: [0, 103808377689281, 315999889281250],
}

ADDITION_CURVES = {
    30: {"n": 30, "m": 2, "P0": (Fraction(169, 4), Fraction(1547, 8)),
         "G": (Fraction(-6), Fraction(-72)), "alpha": 1635, "beta": 5070,
         "congruent_rank": 1, "second_rank": 1},
    60: {"n": 15, "m": 4, "P0": (Fraction(289, 16), Fraction(2737, 64)),
         "G": (Fraction(-15, 4), Fraction(-225, 8)), "alpha": 5070,
         "beta": 17340, "congruent_rank": 1, "second_rank": 1},
    180: {"n": 5, "m": 12, "P0": (Fraction(1681, 144), Fraction(62279, 1728)),
          "G": (Fraction(-4), Fraction(6)), "alpha": 13210, "beta": 33620,
          "congruent_rank": 1, "second_rank": 2},
    84: {"n": 21, "m": 4, "P0": (Fraction(625, 16), Fraction(13175, 64)),
         "G": (Fraction(-3), Fraction(-36)), "alpha": 19194, "beta": 52500,
         "congruent_rank": 1, "second_rank": 2},
    504: {"n": 14, "m": 12, "P0": (Fraction(4225, 144),
                                   Fraction(241345, 1728)),
          "G": (Fraction(18), Fraction(48)), "alpha": 22519, "beta": 59150,
          "congruent_rank": 1, "second_rank": 3},
    1224: {"n": 34, "m": 12, "P0": (Fraction(21025, 144),
                                    Fraction(2964815, 1728)),
           "G": (Fraction(-2), Fraction(-48)), "alpha": 315809,
           "beta": 714850, "congruent_rank": 2, "second_rank": 3},
}


def family8(emit) -> dict:
    # edge factorization identity
    n = 4
    G_, B_, R_, S_ = (Poly.var(n, i) for i in range(4))
    require((((G_ * R_) ** 2 + (B_ * S_) ** 2 - (G_ * S_) ** 2
              - (B_ * R_) ** 2) - (G_ ** 2 - B_ ** 2) * (R_ ** 2 - S_ ** 2))
            .is_zero(), "edge identity")
    require(not (((G_ * R_) ** 2 + (B_ * S_) ** 2 - (G_ * S_) ** 2
                  - (B_ * R_) ** 2)
                 - (G_ ** 2 + B_ ** 2) * (R_ ** 2 - S_ ** 2)).is_zero(),
            "sign-mutated identity rejected")

    # valuation allocation: exhaustive for e in 1..8
    for e in range(1, 9):
        for ai in range(e + 1):
            for aj in range(e + 1):
                vG = min(ai, aj)
                vR = max(ai - aj, 0)
                vS = max(aj - ai, 0)
                vB = e - max(ai, aj)
                require(vG + vR + vS + vB == e and min(vR, vS) == 0,
                        "valuation allocation")

    # interior-vertex table and primitive counts by residue pair
    interior_options = {1: [None, 0, 1, 2], 3: [None], 5: [None, 0],
                        7: [None, 1, 2]}
    expected_counts = {(1, 1): [1, 2, 3], (1, 3): [2, 3], (1, 5): [1, 2, 3],
                       (1, 7): [1, 2, 3], (3, 3): [3], (3, 5): [2, 3],
                       (3, 7): [2, 3], (5, 5): [2, 3], (5, 7): [1, 2, 3],
                       (7, 7): [1, 2, 3]}
    for (rp, rq), want in sorted(expected_counts.items()):
        got = sorted({3 - len({ip, iq} - {None})
                      for ip in interior_options[rp]
                      for iq in interior_options[rq]})
        require(got == want, f"primitive counts residue pair {(rp, rq)}")

    # fixture 1: area 210, two primitive equal-area triangles
    tri_a, tri_b = (20, 21, 29), (12, 35, 37)
    for (u, v, c) in (tri_a, tri_b):
        require(u * u + v * v == c * c and math.gcd(u, v) == 1, "fixture 1")
        require(u * v // 2 == 210, "area 210")
    roots_a = (29 * 29 - 840, 29, 29 * 29 + 840)
    require(roots_a[0] == 1 and is_square(roots_a[0])
            and is_square(roots_a[2]) and sqrt_exact(roots_a[2]) == 41,
            "fixture 1 progression A")
    require(37 * 37 - 840 == 23 ** 2 and 37 * 37 + 840 == 47 ** 2,
            "fixture 1 progression B")
    Nv = 420
    G0 = math.gcd(20, 12)
    R0, S0 = 20 // G0, 12 // G0
    B0 = Nv // (G0 * R0 * S0)
    require((G0, R0, S0, B0) == (4, 5, 3, 7), "fixture 1 edge data")
    require((G0 * R0, B0 * S0, G0 * S0, B0 * R0) == (20, 21, 12, 35),
            "fixture 1 reconstruction")
    F1 = (G0 * G0 - B0 * B0) * (R0 * R0 - S0 * S0)
    require(F1 == -528 == 29 ** 2 - 37 ** 2, "fixture 1 edge value")
    require(support(2 * 840) == [2, 3, 5, 7], "fixture 1 support")

    # fixture 2: area 30600 mixed dropout
    d2 = 122400
    tri0, tri1 = (225, 272, 353), (85, 720, 725)
    for (u, v, c) in (tri0, tri1):
        require(u * u + v * v == c * c, "fixture 2 triangles")
        require(u * v // 2 == 30600, "area 30600")
    require(math.gcd(225, 272) == 1 and math.gcd(85, 720) == 5, "leg gcds")
    require(353 ** 2 - 47 ** 2 == d2 and 497 ** 2 - 353 ** 2 == d2,
            "fixture 2 progression 0")
    require(725 ** 2 - 635 ** 2 == d2 and 805 ** 2 - 725 ** 2 == d2,
            "fixture 2 progression 1")
    core1 = (85 // 5, 720 // 5, 725 // 5)
    require(core1 == (17, 144, 145), "fixture 2 primitive core")
    require(30600 == 1224 * 5 ** 2, "d/4 = A g^2 with A=1224, g=5")
    N2 = d2 // 2
    G2 = math.gcd(225, 85)
    R2, S2 = 225 // G2, 85 // G2
    B2 = N2 // (G2 * R2 * S2)
    require((G2, R2, S2, B2) == (5, 45, 17, 16), "fixture 2 edge data")
    require((G2 * R2, B2 * S2, G2 * S2, B2 * R2) == (225, 272, 85, 720),
            "fixture 2 reconstruction")
    F2 = (G2 * G2 - B2 * B2) * (R2 * R2 - S2 * S2)
    require(F2 == -401016 == 353 ** 2 - 725 ** 2, "fixture 2 edge value")
    require(support(2 * d2) == [2, 3, 5, 17], "fixture 2 support")
    require(not is_square(2 * 725 ** 2 - 353 ** 2)
            and 2 * 725 ** 2 - 353 ** 2 == 926641, "non-closure witness")

    # balanced cores: square progressions, sextics, quotients, integer models
    cores_out = {}
    for area, (u, v, c) in BALANCED_CORES:
        require(u * u + v * v == c * c and math.gcd(u, v) == 1
                and u * v // 2 == area, "core data")
        lam, mu, nu = v - u, c, v + u
        deltav = 2 * u * v
        require(deltav == 4 * area, "delta = 4A")
        require(mu * mu - lam * lam == deltav == nu * nu - mu * mu,
                "square AP with difference 4A")
        c1, c2, c3 = lam ** 4, mu ** 4, nu ** 4
        # sextic identity: f(mu^2+t) f(mu^2-t) = prod(c_i - t^2),
        # f(x) = x(x^2 - delta^2)
        tp = Poly.var(1, 0)
        fplus = (mu * mu + tp) * ((mu * mu + tp) ** 2 - deltav ** 2)
        fminus = (mu * mu - tp) * ((mu * mu - tp) ** 2 - deltav ** 2)
        sextic = (c1 - tp ** 2) * (c2 - tp ** 2) * (c3 - tp ** 2)
        require((fplus * fminus - sextic).is_zero(), f"sextic identity A={area}")
        # quotient factors: L - c_i t^2 = c_i (prod_{j != i} c_j - t^2)
        L = c1 * c2 * c3
        require(((L - c1 * tp ** 2) - c1 * (c2 * c3 - tp ** 2)).is_zero()
                and ((L - c2 * tp ** 2) - c2 * (c1 * c3 - tp ** 2)).is_zero()
                and ((L - c3 * tp ** 2) - c3 * (c1 * c2 - tp ** 2)).is_zero(),
                f"quotient identity A={area}")
        quot_roots = sorted((c2 * c3, c1 * c3, c1 * c2))
        p0 = quot_roots[0]
        d1, d2v = quot_roots[1] - p0, quot_roots[2] - p0
        g = math.gcd(d1, d2v)
        k = max(kk for kk in range(1, math.isqrt(g) + 1) if g % (kk * kk) == 0)
        scaled = [0, d1 // (k * k), d2v // (k * k)]
        require(scaled == FROZEN_SCALED_ROOTS[area],
                f"integer model roots A={area}: {scaled}")
        cores_out[str(area)] = {"core": [u, v, c],
                                "fourth_powers": [c1, c2, c3],
                                "integer_model_roots": scaled}
    # A=6 a-invariants
    require(111 + 93750 == 93861 and 111 * 93750 == 10406250,
            "A=6 a-invariants")

    # central double-balanced fibre: transcript
    tr = parse_transcript(load_frozen(
        "balanced_core6_fibre_magma_v2_29_8.txt").decode("utf-8"))
    require(t_value(tr, "MAGMA_VERSION") == "2 29 8", "core6 magma version")
    require(t_value(tr, "RANK_BOUNDS") == "0 0" and t_value(tr, "RANK") == "0"
            and t_value(tr, "RANK_PROVED") == "true", "core6 rank 0")
    require(parse_int_list(t_value(tr, "TORSION_INVARIANTS")) == [2, 2],
            "core6 torsion")
    require(parse_int_list(t_value(tr, "NONZERO_TORSION_X"))
            == [0, 111, 93750], "core6 torsion x-list")
    require("x^3 - 2926222857*x - 60926629570056"
            in t_value(tr, "MINIMAL_MODEL"), "core6 minimal model (wrapped)")
    require(t_value(tr, "STATUS") == "PASS_INDEPENDENT_MAGMA_REPLAY",
            "core6 status")
    # lifts: torsion x in {0,111,93750} -> u = 16x+625 -> t^2 = L/u
    L6 = 1500625
    tvals = sorted({0} | {sgn * sqrt_exact(L6 // (16 * xv + 625))
                          for xv in (0, 111, 93750) for sgn in (1, -1)})
    require(tvals == [-49, -25, -1, 0, 1, 25, 49], "central allowed t")
    require([tv for tv in tvals if abs(tv) < 1] == [0],
            "central positivity window radius 1")

    # outer core-area-6: sextic identity + certified point list
    tp = Poly.var(1, 0)
    f24 = lambda q: q * (q ** 2 - 576)  # noqa: E731
    require((f24(25 + tp) - (25 + tp) * (tp + 1) * (tp + 49)).is_zero(),
            "outer factor 1")
    require((f24(25 + 2 * tp) - (25 + 2 * tp) * (2 * tp + 1) * (2 * tp + 49))
            .is_zero(), "outer factor 2")
    tro = parse_transcript(load_frozen(
        "outer_core6_gate_magma_v2_29_8.txt").decode("utf-8"))
    require(t_value(tro, "PROVED") == "true"
            and t_value(tro, "NUMBER_POINTS") == "8", "outer proved complete")
    rat_t = parse_int_list(t_value(tro, "RATIONAL_T"))
    require(len(rat_t) == 8, "eight rational points")
    distinct_t = sorted(set(rat_t))
    require(distinct_t == [Fraction(-49), Fraction(-25), Fraction(-49, 2),
                           Fraction(-25, 2), Fraction(-1), Fraction(-1, 2),
                           Fraction(0)], "outer t-list")
    require(t_value(tro, "POSITIVE_DISTINCT_T") in ("[]", "[ ]"),
            "no positive distinct t")
    sex = (tp + 1) * (tp + 25) * (tp + 49) * (2 * tp + 1) * (2 * tp + 25) \
        * (2 * tp + 49)
    for tv in distinct_t:
        val = sex.eval_at((tv,))
        require(rational_sqrt(val) is not None, f"outer point at t={tv}")
    require([tv for tv in distinct_t if tv > Fraction(-1, 2)] == [0],
            "outer positivity leaves only t=0")

    # addition curves H_{n,a}: exact secant algebra + frozen ranks
    # generic addition-law identity on y^2 = x^3 - n^2 x with x2 = 2a - x1:
    # X3 = z^2 - 2a and Y3 = z(x1 - X3) - y1 satisfy Y3^2 = f(X3) modulo
    # the two curve relations, where z = (y2 - y1)/(x2 - x1).
    nv = 5  # x1, y1, y2, a, n
    x1v, y1v, y2v, av, nvv = (Poly.var(nv, i) for i in range(5))
    x2v = 2 * av - x1v
    fx1 = x1v ** 3 - nvv ** 2 * x1v
    fx2 = x2v ** 3 - nvv ** 2 * x2v
    den = x2v - x1v
    znum = y2v - y1v
    X3num = znum ** 2 - 2 * av * den ** 2
    Y3num = znum * (x1v * den ** 2 - X3num) - y1v * den ** 3
    lhs8 = Y3num ** 2
    rhs8 = X3num * (X3num ** 2 - nvv ** 2 * den ** 4)
    diff = (lhs8 - rhs8).reduce_square(1, fx1).reduce_square(2, fx2)
    require(diff.is_zero(), "secant addition identity")

    trc = parse_transcript(load_frozen(
        "central_addition_curves_magma_v2_29_8.txt").decode("utf-8"))
    order = trc["__order__"]
    blocks = {}
    cur = None
    for key, val in order:
        if key == "BEGIN":
            cur = val
            blocks[cur] = {}
        elif key == "END":
            cur = None
        elif cur is not None:
            blocks[cur][key] = val
    require(list(blocks) == ["A30", "A60", "A180", "A84", "A504", "A1224"],
            "central MW block order")
    jac_ranks = {}
    for area, spec in sorted(ADDITION_CURVES.items()):
        ncong = spec["n"]
        m = spec["m"]
        require(4 * area == ncong * m * m, "4A = n m^2 with n squarefree")
        require(all(e == 1 for e in factorize(ncong).values()),
                "n squarefree")
        core = dict(BALANCED_CORES)[area]
        a_val = Fraction(core[2] ** 2, m * m)
        require(a_val == spec["P0"][0], "a = c^2/m^2")
        An = -ncong * ncong
        require(ec_on(An, spec["P0"]) and ec_on(An, spec["G"]),
                "P0, G on E_n")
        minus2G = ec_neg(ec_mul(An, 2, spec["G"]))
        require(minus2G == spec["P0"], "P0 = -2G")
        pa = (2 * a_val - ncong) * (2 * a_val)
        pb = (2 * a_val - ncong) * (2 * a_val + ncong)
        pc = (2 * a_val) * (2 * a_val + ncong)
        ralpha = Fraction(spec["alpha"]) / (pb - pa)
        rbeta = Fraction(spec["beta"]) / (pc - pa)
        require(ralpha == rbeta and rational_sqrt(ralpha) is not None,
                "alpha/beta scale is a common rational square")
        blk = blocks[f"A{area}"]
        lo, hi = blk["CONGRUENT_RANK"].split()
        require(lo == hi == str(spec["congruent_rank"]),
                f"congruent rank A{area}")
        lo2, hi2 = blk["ADDITION_SECOND_QUOTIENT_RANK"].split()
        require(lo2 == hi2 == str(spec["second_rank"]),
                f"second quotient rank A{area}")
        require(blk["FIXED_CLASS_MINUS_2G"] == "true", "fixed class -2G")
        require(parse_int_list(blk["ADDITION_SECOND_QUOTIENT_TORSION"])
                == [2, 2], "second quotient torsion")
        jac_ranks[str(area)] = spec["congruent_rank"] + spec["second_rank"]
    require([jac_ranks[str(a)] for a in (30, 60, 180, 84, 504, 1224)]
            == [2, 2, 3, 3, 4, 5], "Jacobian ranks 2,2,3,3,4,5")

    # singleton fake two-Selmer sets for areas 30 and 60 (untruncated)
    selmer = {}
    for area, name in ((30, "area30_magma.txt"),
                       (60, "area60_magma.txt")):
        trs = parse_transcript(load_frozen(name).decode("utf-8"))
        require(t_value(trs, "MAGMA_VERSION") == "2 29 8",
                f"Magma version A{area}")
        require(t_value(trs, "SELMER_SIZE") == "1", f"selmer size A{area}")
        require(t_value(trs, "SELMER_SET").replace(" ", "") == "{0}",
                f"selmer set A{area}")
        require(t_value(trs, "DELTA_IMAGE") == "0", f"delta image A{area}")
        require(t_value(trs, "STATUS") == "DONE", f"selmer status A{area}")
        selmer[str(area)] = {
            "engine": "Magma V2.29-8",
            "size": 1,
            "set": [0],
        }
    emit("family8: edge identity, both fixtures, seven balanced cores, both "
         "closed core-6 fibres and the six addition curves verified "
         "(Jacobian ranks 2,2,3,3,4,5; fake Selmer singletons)")
    return {
        "edge_identity": True,
        "fixtures": {"area_210_edge_value": F1,
                     "area_30600_edge_value": F2,
                     "area_30600_nonclosure_witness": 926641},
        "balanced_cores": cores_out,
        "central_allowed_t": tvals,
        "outer_t_list": [fstr(tv) for tv in distinct_t],
        "jacobian_ranks": jac_ranks,
        "fake_selmer_singletons": selmer,
    }


# --------------------------------------------------------------------------
# family 9 -- Appendix A: the frozen (8,7) height census, replayed from
# scratch as a second independent enumerator (full progressions from root
# triples, partial ones by direct scan, assembly on the normal form, exact
# D4 quotient).
# --------------------------------------------------------------------------

def family9_census(emit) -> dict:
    def full_aps(height):
        out = []
        for t in range(2, height + 1):
            for r in range(1, t):
                s2, rem = divmod(r * r + t * t, 2)
                if rem == 0 and is_square(s2):
                    s = sqrt_exact(s2)
                    if r < s < t:
                        out.append((r, s, t))
        return sorted(out)

    aps46 = full_aps(46)
    aps47 = full_aps(47)
    require(len(aps46) == 12, f"{len(aps46)} full progressions at height 46")
    require(len(aps47) == 13, f"{len(aps47)} full progressions at height 47")
    diffs46 = [s * s - r * r for (r, s, t) in aps46]
    require(len(set(diffs46)) == 12,
            "height 46: all common differences distinct, census empty")
    diffs47 = [s * s - r * r for (r, s, t) in aps47]
    doubled = sorted({dv for dv in diffs47 if diffs47.count(dv) >= 2})
    require(doubled == [840], "only difference 840 carries two full "
            "progressions at height 47")
    fulls = [ap for ap in aps47 if ap[1] ** 2 - ap[0] ** 2 == 840]
    require(fulls == [(1, 29, 41), (23, 37, 47)], "the two full progressions")

    partial_candidates = []
    for a in range(1, 1370):
        trip = (a, a + 840, a + 1680)
        squares = [v for v in trip if is_square(v)]
        if len(squares) == 2 and max(sqrt_exact(v) for v in squares) <= 47:
            partial_candidates.append(trip)
    require(partial_candidates == [
        (121, 961, 1801), (169, 1009, 1849), (256, 1096, 1936),
        (841, 1681, 2521), (1369, 2209, 3049),
    ], f"partial candidates {partial_candidates}")

    def grid(x0, x1, x2):
        return ((x1, x2 + 840, x0 - 840),
                (x2 - 840, x0, x1 + 840),
                (x0 + 840, x1 - 840, x2))

    arrays = set()
    usable_partials = []
    for part in partial_candidates:
        arrays_from_part = set()
        cents = [841, 1369, part[1]]
        for i0 in range(3):
            rest = [c for j, c in enumerate(cents) if j != i0]
            for x1, x2 in (tuple(rest), tuple(rest[::-1])):
                g = grid(cents[i0], x1, x2)
                entries = [v for row in g for v in row]
                if (not all(v > 0 for v in entries)
                        or len(set(entries)) != 9
                        or sum(1 for v in entries if is_square(v)) != 8
                        or max(sqrt_exact(v) for v in entries if is_square(v)) > 47):
                    continue
                total = cents[i0] + x1 + x2
                lines = ([sum(row) for row in g]
                         + [sum(col) for col in zip(*g)]
                         + [g[0][0] + g[1][1] + g[2][2]])
                require(all(v == total for v in lines),
                        "census seven common lines")
                require(g[0][2] + g[1][1] + g[2][0] == 3 * cents[i0] != total,
                        "census failed antidiagonal")
                arrays_from_part.add(g)
        if arrays_from_part:
            usable_partials.append(part)
            arrays.update(arrays_from_part)
    require(usable_partials == [(121, 961, 1801), (169, 1009, 1849),
                                (256, 1096, 1936)],
            f"distinct compatible partials {usable_partials}")
    require(len(arrays) == 18, f"{len(arrays)} labelled arrays")

    def d4_canonical(g):
        def rot(m):
            return tuple(zip(*m[::-1]))
        forms = []
        m = g
        for _ in range(4):
            m = rot(m)
            forms.append(m)
            forms.append(tuple(tuple(row[::-1]) for row in m))
        return min(forms)

    classes = sorted({d4_canonical(g) for g in arrays})
    require(len(classes) == 9, f"{len(classes)} D4 classes")
    nonsq_centre = [c for c in classes if not is_square(c[1][1])]
    require(len(nonsq_centre) == 2, "two centre-nonsquare classes")
    emit("family9: Appendix-A census replayed from scratch -- 12/13 full "
         "progressions at heights 46/47, difference 840 unique, 5 raw / "
         "3 distinct-compatible partials, "
         "18 arrays = 9 D4 classes (2 centre-nonsquare)")
    return {
        "full_progressions_h46": len(aps46),
        "full_progressions_h47": len(aps47),
        "doubled_difference": 840,
        "full_pair_roots": [[1, 29, 41], [23, 37, 47]],
        "partial_progression_candidates": [list(t) for t in partial_candidates],
        "partial_progressions": [list(t) for t in usable_partials],
        "labelled_arrays": 18,
        "d4_classes": 9,
        "centre_nonsquare_classes": 2,
        "canonical_representatives": [[list(r) for r in c] for c in classes],
    }


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", required=True, type=Path)
    ap.add_argument("--log", required=True, type=Path)
    ap.add_argument(
        "--refresh-expected",
        action="store_true",
        help=("maintainer-only: rewrite the frozen expected JSON, but only "
              "after the live digest matches the source-pinned constant"),
    )
    args = ap.parse_args()

    started = time.perf_counter()
    log: list[str] = []

    def emit(m: str) -> None:
        line = f"[{time.perf_counter() - started:7.3f}s] {m}"
        print(line, flush=True)
        log.append(line)

    frozen = {}
    for name in sorted(FROZEN_FILES):
        data = load_frozen(name)
        sha, size = FROZEN_FILES[name]
        frozen[name] = {"sha256": sha, "bytes": size}
    emit(f"frozen layer: {len(frozen)} files digest-verified "
         "(external-CAS records + inputs)")

    families = {
        "family0_line_sum_lattice": family0_line_sum_lattice(emit),
        "family1_quartic_witness": family1_quartic_witness(emit),
        "family2_infinite_families": {
            "retraction": family2_retraction(emit),
            "bridge": family2_bridge(emit),
            "elliptic_lift": family2_lift(emit),
        },
        "family3_interaction_surface": family3(emit),
        "family4_fibre_stop": family4(emit),
        "family4b_bremner_shadow": family4b_bremner_shadow(emit),
        "family5_half_class_stop": family5(emit),
        "family6_support_law": family6(emit),
        "family7_three_prime_exclusion": family7(emit),
        "family8_four_prime_frontier": family8(emit),
        "family9_height_census": family9_census(emit),
    }

    payload = {
        "schema": "FCIG-NEARMISS-SUPPORT-CERTIFICATES-v1",
        "status": "PASS",
        "terminal": "MAIN_PAPER_EXACT_CERTIFICATES_PASS",
        "claim_scope": ("exact finite certificates and frozen-transcript "
                        "digests for the theorems of the main paper; no "
                        "novelty or firstness claim; nothing here proves or "
                        "refutes the existence of a 3x3 magic square of "
                        "squares"),
        "engine_policy": ("python standard library only; exact integer and "
                          "rational arithmetic, plus deterministic Decimal "
                          "quadrature used only to corroborate a displayed "
                          "decimal; external computer algebra "
                          "enters only as hash-verified frozen records and "
                          "is never executed"),
        "families": families,
        "frozen_files": frozen,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    require(digest == EXPECTED_CERTIFICATE_SHA256,
            f"live output digest {digest} differs from the pinned constant "
            "(fail closed)")
    expected = CERT / "expected_verification.json"
    if args.refresh_expected:
        expected.write_text(text, encoding="utf-8", newline="\n")
    require(expected.exists(),
            "certificates/expected_verification.json is missing (fail closed)")
    require(text.encode("utf-8") == expected.read_bytes(),
            "output differs from certificates/expected_verification.json "
            "(fail closed)")
    emit("self-check: digest matches the pinned constant and the frozen "
         "certificate byte for byte")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.log.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8", newline="\n")
    emit(f"certificate_sha256={digest.upper()}")
    emit("PASS")
    args.log.write_text("\n".join(log) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
