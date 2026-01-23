# Governing Equations and Modeling Assumptions

## Process Description
This project models a non-isothermal batch reactor carrying out consecutive
first-order liquid-phase reactions:

**A → B → C**

The objective is to maximize the concentration of intermediate B by controlling
the reactor temperature profile and batch time.

This formulation is representative of batch pharmaceutical and specialty
chemical manufacturing processes where temperature history strongly affects
yield and impurity formation.

The mechanistic model follows standard formulations commonly presented in
process dynamics and control literature.

---

## Assumptions
- Perfect mixing in the reactor
- Constant reactor volume
- Constant density and heat capacity
- Liquid-phase reactions
- No inflow or outflow during the batch
- Lumped heat transfer model
- Jacket temperature is treated as a known input

---

## Reaction Kinetics

The reactions are first-order with Arrhenius temperature dependence:

$$k_1(T) = k_{0,1} \exp\left(\frac{-E_1}{RT}\right)$$

$$k_2(T) = k_{0,2} \exp\left(\frac{-E_2}{RT}\right)$$

**Where:**
- $k_1, k_2$ = reaction rate constants
- $k_{0,1}, k_{0,2}$ = pre-exponential factors
- $E_1, E_2$ = activation energies
- $R$ = universal gas constant
- $T$ = reactor temperature

---

## Mass Balances

### Component A:
$$\frac{dC_A}{dt} = -k_1(T) C_A$$

### Component B:
$$\frac{dC_B}{dt} = k_1(T) C_A - k_2(T) C_B$$

### Component C:
$$\frac{dC_C}{dt} = k_2(T) C_B$$

**Where:**
- $C_A, C_B, C_C$ = concentrations of components A, B, and C
- $t$ = time

---

## Energy Balance

The energy balance for the reacting mass is:

$$\rho C_p \frac{dT}{dt} = -\Delta H_1 k_1(T) C_A - \Delta H_2 k_2(T) C_B + \frac{UA}{V}(T_j - T)$$

**Where:**
- $\rho$ = density
- $C_p$ = heat capacity
- $\Delta H_1, \Delta H_2$ = heats of reaction
- $U$ = overall heat transfer coefficient
- $A$ = heat transfer area
- $V$ = reactor volume
- $T_j$ = jacket temperature
- $T$ = reactor temperature

---

## Notes on Extension

This model can be extended to include:
- Explicit jacket energy balance
- Temperature controller dynamics
- Measurement noise and disturbances
- Hybrid data-driven correction terms

These extensions are consistent with digital twin and advanced process
modeling workflows.
