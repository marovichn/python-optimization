import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import linprog

c = np.array([-120, -70, -90])
A_ub = np.array([[3, 1, 2],
                 [4, 2, 3],
                 [2, 1, 2],
                 [1, 1, 1]])
bounds = [(0, None), (10, None), (0, 40)]

pakovanje_vrednosti = np.arange(70, 226, 5)
profit, shadow = [], []

for pakovanje in pakovanje_vrednosti:
    b_ub = np.array([240, 360, 180, pakovanje])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if res.success:
        profit.append(-res.fun)
        shadow.append(-res.ineqlin.marginals[0])   # okrecemo znak (max problem)
    else:
        profit.append(np.nan)
        shadow.append(np.nan)

profit = np.array(profit)
shadow = np.array(shadow)

# numericki nagib izmedju susednih tacaka
nagib = np.diff(profit) / np.diff(pakovanje_vrednosti)

print(f"{'pakovanje':>5} {'profit':>9} {'shadow':>7}")
for d, p, s in zip(pakovanje_vrednosti, profit, shadow):
    print(f"{d:5d} {p:9.1f} {s:7.2f}")

# tacke loma: gde se shadow price menja
print("\nPromene shadow price-a (lomovi):")
for i in range(1, len(shadow)):
    if not np.isclose(shadow[i], shadow[i-1]):
        print(f"  izmedju pakovanja={pakovanje_vrednosti[i-1]} i {pakovanje_vrednosti[i]}: {shadow[i-1]:.2f} -> {shadow[i]:.2f}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
ax1.plot(pakovanje_vrednosti, profit, "o-", ms=3, color="#188038")
ax1.set_ylabel("Optimalni profit (€)")
ax1.set_title("Osetljivost profita na količinu pakovanja")
ax1.grid(alpha=0.3)

ax2.step(pakovanje_vrednosti, shadow, where="mid", color="#188038")
ax2.plot(pakovanje_vrednosti, shadow, "o", ms=3, color="#188038")
ax2.set_xlabel("Raspoloživo pakovanja (h)")
ax2.set_ylabel("Shadow price pakovanja (€/h)")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("osetljivost2.png", dpi=130)