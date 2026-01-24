import numpy as np
import matplotlib.pyplot as plt
from mechanistic_model import Params, simulate_batch, default_Tj_profile

# Example parameters (not "truth"—just plausible scales)
p = Params(
    k01=2.0e6,    E1=8.0e4,   # A->B
    k02=1.0e7,    E2=9.0e4,   # B->C
    dH1=-5.0e4,   dH2=-2.0e4, # J/mol (exothermic)
    rhoCp=4.2e3,  # J/(L*K) ~ water-like
    UA_over_V=50.0,  # J/(L*s*K) tuneable
)

# Initial conditions: CA0, CB0, CC0, T0
y0 = np.array([1.0, 0.0, 0.0, 350.0])  # mol/L, K


# Piecewise profile
def Tj(t: float) -> float:
    # Example: heat up, hold, cool down (Kelvin)
    if t < 600:        # first 10 min
        return 320 + (350 - 320) * (t / 600)
    elif t < 2400:     # next 30 min
        return 350
    else:              # last 20 min
        return 330

t_eval = np.linspace(0, 3600, 1000)  # 1 hour batch

print("Running simulation...")
out = simulate_batch((t_eval[0], t_eval[-1]), y0, p, Tj, t_eval=t_eval)

# Analyze results
max_CB_idx = np.argmax(out["CB"])
max_CB = out["CB"][max_CB_idx]
time_at_max = out["t"][max_CB_idx]

print("-" * 30)
print("Simulation Complete")
print("-" * 30)
print(f"Max Concentration of B: {max_CB:.4f} mol/L")
print(f"Time at Max B:          {time_at_max:.1f} s")
print(f"Final Temperature:      {out['T'][-1]:.2f} K")
print("-" * 30)

# --- Plotting ---
print("Generating plot...")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot Concentrations
ax1.plot(out["t"], out["CA"], label="CA (Reactant)")
ax1.plot(out["t"], out["CB"], label="CB (Product)", linewidth=2)
ax1.plot(out["t"], out["CC"], label="CC (Impurity/Byproduct)")
ax1.set_ylabel("Concentration (mol/L)")
ax1.set_title("Batch Reactor - Concentration Profiles")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot Temperature
ax2.plot(out["t"], out["T"], 'r-', label="Reactor Temp (T)")
# Calculate and plot Jacket Temp for reference
Tj_vals = [Tj(t) for t in out["t"]]
ax2.plot(out["t"], Tj_vals, 'b--', label="Jacket Temp (Tj)", alpha=0.7)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Temperature (K)")
ax2.set_title("Temperature Profile")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
output_filename = "simulation_results.png"
plt.savefig(output_filename)
print(f"Plot saved to '{output_filename}'")
