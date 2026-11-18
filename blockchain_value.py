"""The capability-based valuation model of "The architecture of blockchain value" (Papadogiannis, 2026).

Equation numbers refer to the published article, Front. Blockchain 9:1747512,
https://doi.org/10.3389/fbloc.2026.1747512. Standard library only.

    from blockchain_value import benchmark_value, network_value, Capability, scaling_law

    benchmark_value(K=50, eta=0.75)            # Equation (14) with phi = u = N = 1  ->  968.75
    scaling_law("reed", 10)                     # V(u) = 2**u                         ->  1024.0

The model is stylized. Its parameters are illustrations, not estimates, and nothing here values a
specific network or token.
"""
from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Mapping, Optional, Sequence, Tuple, Union

SCALING_LAWS = ("sarnoff", "metcalfe", "reed")


def scaling_law(law: str, u: float) -> float:
    """Network value V(u) under the three scaling laws of Section 8 and Figure 8.

    sarnoff: V(u) = u        metcalfe: V(u) = u**2        reed: V(u) = 2**u
    """
    if law == "sarnoff":
        return float(u)
    if law == "metcalfe":
        return float(u) ** 2
    if law == "reed":
        return 2.0 ** float(u)
    raise ValueError(f"unknown scaling law {law!r}; use one of {SCALING_LAWS}")


def network_effect(law: str) -> Callable[[float], float]:
    """Network-effect multiplier N(u) that gives V(u) = u N(u) the shape of a scaling law.

    With one capability and phi = 1, Equation (6) reads v = u N(u). So Sarnoff is N(u) = 1,
    Metcalfe is N(u) = u and Reed is N(u) = 2**u / u.
    """
    if law not in SCALING_LAWS:
        raise ValueError(f"unknown scaling law {law!r}; use one of {SCALING_LAWS}")
    return lambda u: scaling_law(law, u) / float(u)


@dataclass(frozen=True)
class Capability:
    """One capability f of a blockchain: a service it delivers at consensus quality.

    phi       value per unit (price, quality and scarcity in one constant), phi_f
    adoption  share of the global user base that uses it, a_f(u), between 0 and 1
    N         network-effect multiplier N_f, a function of the capability's own user base
    """
    name: str
    phi: float = 1.0
    adoption: float = 1.0
    N: Callable[[float], float] = lambda u_f: 1.0

    def user_base(self, u: float) -> float:
        """Equation (5): u_f = a_f(u) u."""
        return self.adoption * u

    def value(self, u: float) -> float:
        """Equation (6): v_f(u_f) = phi_f u_f N_f(u_f)."""
        u_f = self.user_base(u)
        return self.phi * u_f * self.N(u_f)


Eta = Union[float, Mapping[Tuple[str, str], float]]


def network_value(capabilities: Sequence[Capability], u: float, eta: Eta = 0.0,
                  V0: Optional[float] = None) -> float:
    """Equation (7): total network value of a blockchain with global user base u.

        V(u) = sum_f v_f(u_f)  +  sum_{f<g} eta_fg v_f(u_f) v_g(u_g) / V0(u)

    eta  pairwise complementarity: one number for all pairs, or a mapping {(name_f, name_g): eta_fg}
         in which a missing pair counts as zero. Each eta_fg must be >= 0.
    V0   normalization scale with units of value. It is needed whenever some eta_fg is positive.
         The symmetric benchmarks of the article use V0 = phi u N(u), the value of one capability.

    A single capability gives Equation (8); Equations (9) and (10) are this function applied to the
    capability set and the complementarities of a multi- or meta-capability network.
    """
    names = [c.name for c in capabilities]
    if len(set(names)) != len(names):
        raise ValueError("capability names must be distinct")
    v = {c.name: c.value(u) for c in capabilities}
    direct = sum(v.values())
    composability = 0.0
    for f, g in combinations(names, 2):
        if isinstance(eta, Mapping):
            e = eta.get((f, g), eta.get((g, f), 0.0))
        else:
            e = eta
        if e < 0:
            raise ValueError("complementarities must be non-negative")
        if e == 0:
            continue
        if V0 is None or V0 <= 0:
            raise ValueError("a positive V0 is required when a complementarity is positive")
        composability += e * v[f] * v[g] / V0
    return direct + composability


def benchmark_value(K: int, eta: float = 0.0, phi: float = 1.0, u: float = 1.0, N: float = 1.0) -> float:
    """Equation (14): value with K capabilities under the symmetric benchmark.

        V(u) = phi u N(u) [ K + eta K (K - 1) / 2 ]

    Assumes full adoption, the same per-unit value phi for every capability, a common network-effect
    multiplier N = N(u), one complementarity eta for every pair, and V0 = phi u N(u).
    eta = 0 gives Benchmark 1, Equations (11) to (13). K = 1 gives Equation (15).
    With phi = u = N = 1 this is the normalized value of Equations (18), (19) and Figure 5.
    """
    if K < 1:
        raise ValueError("K must be at least 1")
    if eta < 0:
        raise ValueError("eta must be non-negative")
    return phi * u * N * (K + eta * K * (K - 1) / 2.0)


def complementarity_share(K: int, eta: float) -> float:
    """Share of the Equation (14) value that comes from the pairwise term rather than the direct term."""
    pairs = eta * K * (K - 1) / 2.0
    return pairs / (K + pairs)


# ---------------------------------------------------------------------------------------------
# Beyond the published figures. The article's figures use the symmetric benchmark, in which every
# capability is worth the same. The functions below apply Equation (7), as published, to capabilities
# of unequal value while holding their total stand-alone value fixed, so that the only thing that
# changes is the bonus from pairs. The way the total is split is a choice made here for illustration.

def split_values(K: int, top_share: float) -> list:
    """Stand-alone values of K capabilities that add up to K, when the largest holds top_share of the total.

    The other K - 1 capabilities share the rest equally. A top_share at or below 1 / K gives equal
    values of 1 each, the article's benchmark.
    """
    if K < 1:
        raise ValueError("K must be at least 1")
    if not 0 <= top_share < 1 and K > 1:
        raise ValueError("top_share must be at least 0 and below 1")
    if K == 1:
        return [1.0]
    p = max(top_share, 1.0 / K)
    return [p * K] + [(1.0 - p) * K / (K - 1)] * (K - 1)


def unequal_value(K: int, eta: float, top_share: float) -> float:
    """Equation (7) for K capabilities with the same total stand-alone value as in the benchmark, split unequally.

    Values are split_values(K, top_share), one complementarity eta applies to every pair, and the
    normalization V0 is the average capability value (which is the article's V0 = phi u N when all
    capabilities are equal). The direct term is K whatever the split. The pair term is
    eta K**2 (1 - H) / 2, where H is the sum of squared value shares: it is largest when the values
    are equal (H = 1 / K, Equation 14) and falls to zero as one capability takes all the value.
    """
    values = split_values(K, top_share)
    caps = [Capability(f"c{i}", phi=v) for i, v in enumerate(values)]
    return network_value(caps, u=1.0, eta=eta, V0=sum(values) / K)
