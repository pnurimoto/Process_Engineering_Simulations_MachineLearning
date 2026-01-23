from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Tuple
import numpy as np
from scipy.integrate import solve_ivp


R_GAS = 8.314  # J/(mol*K)


@dataclass(frozen=True)
class Params:
    # Arrhenius parameters (units depend on reaction order; here first-order => 1/s)
    k01: float      # 1/s
    E1: float       # J/mol
    k02: float      # 1/s
    E2: float       # J/mol

    # Reaction heats (J/mol). Negative for exothermic.
    dH1: float      # J/mol
    dH2: float      # J/mol

    # Thermal properties lumped on reactor contents
    rhoCp: float    # J/(L*K)  (density * heat capacity)
    UA_over_V: float  # J/(L*s*K)  (UA divided by reactor volume)


def arrhenius(k0: float, E: float, T: float) -> float:
    """Arrhenius rate constant k(T) = k0 * exp(-E/(R*T))."""
    return k0 * np.exp(-E / (R_GAS * T))


def default_Tj_profile(Tj_const: float) -> Callable[[float], float]:
    """Returns a constant jacket temperature function Tj(t)."""
    def Tj(t: float) -> float:
        return Tj_const
    return Tj


def odes(t: float, y: np.ndarray, p: Params, Tj: Callable[[float], float]) -> np.ndarray:
    """
    y = [CA, CB, CC, T]
    CA, CB, CC in mol/L
    T in K
    """
    CA, CB, CC, T = y

    k1 = arrhenius(p.k01, p.E1, T)  # 1/s
    k2 = arrhenius(p.k02, p.E2, T)  # 1/s

    r1 = k1 * CA   # mol/(L*s)
    r2 = k2 * CB   # mol/(L*s)

    dCA = -r1
    dCB = r1 - r2
    dCC = r2

    # Heat generation term: (-dH)*rate
    # If dH is negative (exothermic), -dH*r is positive => heats up reactor (as expected)
    Q_rxn = (-p.dH1) * r1 + (-p.dH2) * r2            # J/(L*s)
    Q_ht  = p.UA_over_V * (Tj(t) - T)                # J/(L*s)

    dT = (Q_rxn + Q_ht) / p.rhoCp                    # K/s

    return np.array([dCA, dCB, dCC, dT], dtype=float)


def simulate_batch(
    t_span: Tuple[float, float],
    y0: np.ndarray,
    params: Params,
    Tj: Callable[[float], float],
    t_eval: np.ndarray | None = None,
    method: str = "BDF",
    rtol: float = 1e-7,
    atol: float = 1e-9,
) -> Dict[str, np.ndarray]:
    """
    Simulate the batch reactor.
    Returns dict with time and state trajectories.
    """
    if t_eval is None:
        t_eval = np.linspace(t_span[0], t_span[1], 500)

    sol = solve_ivp(
        fun=lambda t, y: odes(t, y, params, Tj),
        t_span=t_span,
        y0=y0,
        t_eval=t_eval,
        method=method,   # BDF handles stiffness well (Arrhenius often causes stiffness)
        rtol=rtol,
        atol=atol,
    )

    if not sol.success:
        raise RuntimeError(f"ODE solve failed: {sol.message}")

    CA, CB, CC, T = sol.y

    return {
        "t": sol.t,
        "CA": CA,
        "CB": CB,
        "CC": CC,
        "T": T,
    }
