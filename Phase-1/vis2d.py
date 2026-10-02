import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from scipy.optimize import linprog

c = np.array([-120, -70, -90])
A_ub = np.array([[3, 1, 2],
                 [4, 2, 3],
                 [2, 1, 2],
                 [1, 1, 1]])
bounds = [(0, None), (10, None), (0, 40)]
imena = ["drvo", "stolarija", "farbanje", "pakovanje"]

drvo_v = np.arange(100, 351, 5)
pak_v = np.arange(70, 226, 5)

# 2D mreza: red = pakovanje, kolona = drvo
profit = np.full((len(pak_v), len(drvo_v)), np.nan)
sp_drvo = np.full_like(profit, np.nan)
sp_pak = np.full_like(profit, np.nan)
rezim = np.empty(profit.shape, dtype=object)   # skup aktivnih ogranicenja

for i, pak in enumerate(pak_v):
    for j, drvo in enumerate(drvo_v):
        b_ub = np.array([drvo, 360, 180, pak])
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
        if res.success:
            profit[i, j] = -res.fun
            sp_drvo[i, j] = -res.ineqlin.marginals[0]
            sp_pak[i, j] = -res.ineqlin.marginals[3]
            aktivna = [n for n, s in zip(imena, res.slack) if np.isclose(s, 0)]
            rezim[i, j] = " + ".join(aktivna) if aktivna else "nista"

# kategorije uskih grla -> brojevi za bojenje
kategorije = sorted({r for r in rezim.ravel() if r is not None})
kod = {k: n for n, k in enumerate(kategorije)}
mapa = np.array([[kod.get(r, np.nan) for r in red] for red in rezim], dtype=float)

print("Rezimi uskih grla (aktivna ogranicenja):")
for k in kategorije:
    print(f"  {k:<35} {np.sum(mapa == kod[k])} tacaka")

extent = [drvo_v[0] - 2.5, drvo_v[-1] + 2.5, pak_v[0] - 2.5, pak_v[-1] + 2.5]
kw = dict(origin="lower", extent=extent, aspect="auto")

fig, axs = plt.subplots(2, 2, figsize=(14, 10), sharex=True, sharey=True)

# 1. profit
ax = axs[0, 0]
im = ax.imshow(profit, cmap="Greens", **kw)
cs = ax.contour(drvo_v, pak_v, profit, colors="#188038", linewidths=0.8)
ax.clabel(cs, fmt="%d", fontsize=7)
fig.colorbar(im, ax=ax, label="€")
ax.set_title("Optimalni profit")

# 2. usko grlo
ax = axs[0, 1]
boje = plt.cm.Set2(np.linspace(0, 1, max(len(kategorije), 3)))
ax.imshow(mapa, cmap=ListedColormap(boje[:len(kategorije)]), vmin=-0.5,
          vmax=len(kategorije) - 0.5, **kw)
ax.legend(handles=[Patch(color=boje[n], label=k) for k, n in kod.items()],
          fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, title="aktivna ograničenja")
ax.set_title("Usko grlo (aktivna ograničenja)")

# 3. i 4. shadow prices
for ax, data, naslov in [(axs[1, 0], sp_drvo, "Shadow price drveta (€/m³)"),
                         (axs[1, 1], sp_pak, "Shadow price pakovanja (€/h)")]:
    im = ax.imshow(data, cmap="Greens", **kw)
    fig.colorbar(im, ax=ax)
    ax.set_title(naslov)

for ax in axs[1]:
    ax.set_xlabel("Raspoloživo drvo (m³)")
for ax in axs[:, 0]:
    ax.set_ylabel("Raspoloživo pakovanje (h)")
    
# oznaka originalne tacke (240, 100)
for ax in axs.ravel():
    ax.plot(240, 100, "k*", ms=10)

plt.tight_layout(rect=(0, 0.02, 1, 1))
plt.savefig("osetljivost2d.png", dpi=260)