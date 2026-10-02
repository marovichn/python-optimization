import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.optimize import linprog

BOJA = "#188038"
c = np.array([-120, -70, -90])
A_ub = np.array([[3, 1, 2],
                 [4, 2, 3],
                 [2, 1, 2],
                 [1, 1, 1]])
bounds = [(0, None), (10, None), (0, 40)]
imena = ["drvo", "stolarija", "farbanje", "pakovanje"]

# isti opseg za drvo i pakovanje: obe vrednosti = t
t_v = np.arange(70, 351, 2)
profit, sp_drvo, sp_pak, rezim = [], [], [], []

for t in t_v:
    b_ub = np.array([t, 360, 180, t])          # drvo = pakovanje = t
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    profit.append(-res.fun)
    sp_drvo.append(-res.ineqlin.marginals[0])
    sp_pak.append(-res.ineqlin.marginals[3])
    aktivna = [n for n, s in zip(imena, res.slack) if np.isclose(s, 0)]
    rezim.append(" + ".join(aktivna))

profit, sp_drvo, sp_pak = map(np.array, (profit, sp_drvo, sp_pak))

# ispis tacaka gde se rezim menja
print("Promene usko grla:")
for i in range(1, len(t_v)):
    if rezim[i] != rezim[i - 1]:
        print(f"  t={t_v[i-1]}..{t_v[i]}: [{rezim[i-1]}]  ->  [{rezim[i]}]")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True,
                               gridspec_kw={"height_ratios": [2, 1.4]})

# pozadina: usko grlo kao obojene trake
kat = list(dict.fromkeys(rezim))
boje = dict(zip(kat, plt.cm.Set2(np.linspace(0, 1, max(len(kat), 3)))))
for ax in (ax1, ax2):
    for i, t in enumerate(t_v):
        ax.axvspan(t - 1, t + 1, color=boje[rezim[i]], alpha=0.35, lw=0)

ax1.plot(t_v, profit, "o-", ms=3, color=BOJA)
ax1.set_ylabel("Optimalni profit (€)")
ax1.set_title("Profit kad se drvo i pakovanje menjaju zajedno (isti opseg)")
ax1.grid(alpha=0.3)
ax1.legend(handles=[Patch(color=boje[k], alpha=0.5, label=k) for k in kat],
           fontsize=8, title="aktivna ograničenja", loc="upper left")

ax2.plot(t_v, sp_drvo, "-", color=BOJA, label="shadow price drveta (€/m³)")
ax2.plot(t_v, sp_pak, "--", color=BOJA, label="shadow price pakovanja (€/h)")
ax2.set_xlabel("t = raspoloživo drvo = raspoloživo pakovanje")
ax2.set_ylabel("Shadow price (€)")
ax2.legend(fontsize=8)
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig("osetljivost3.png", dpi=130)