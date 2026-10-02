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
STOLARIJA = 360                                  # fiksirano

# razliciti opsezi i koraci po resursu
drvo_v = np.arange(160, 321, 20)                 # korak 20
pak_v  = np.arange(70, 131, 10)                  # korak 10
farb_v = np.arange(150, 211, 5)                  # korak 5 (sitniji, jer duze traje)

D, P, F = np.meshgrid(drvo_v, pak_v, farb_v, indexing="ij")
profit = np.full(D.shape, np.nan)
rezim = np.empty(D.shape, dtype=object)

for idx in np.ndindex(D.shape):
    b_ub = np.array([D[idx], STOLARIJA, F[idx], P[idx]])
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if res.success:
        profit[idx] = -res.fun
        akt = [n for n, s in zip(imena, res.slack) if np.isclose(s, 0)]
        rezim[idx] = " + ".join(akt)

print(f"Resenih LP-ova: {np.sum(~np.isnan(profit))} od {profit.size}")
kat = sorted({r for r in rezim.ravel() if r})
for k in kat:
    print(f"  {k:<40} {np.sum(rezim == k)}")

fig = plt.figure(figsize=(9, 15))

# 1. 3D: boja = profit
ax1 = fig.add_subplot(211, projection="3d")
sc = ax1.scatter(D.ravel(), P.ravel(), F.ravel(), c=profit.ravel(),
                 cmap="Greens", s=28, depthshade=False)
fig.colorbar(sc, ax=ax1, shrink=0.6, pad=0.08, label="Profit (€)")
ax1.set_title("Optimalni profit")

# 2. 3D: boja = usko grlo
ax2 = fig.add_subplot(212, projection="3d")
boje = dict(zip(kat, plt.cm.tab10(np.arange(len(kat)))))
for k in kat:
    m = (rezim == k)
    ax2.scatter(D[m], P[m], F[m], color=boje[k], s=28, depthshade=False)
ax2.legend(handles=[Patch(color=boje[k], label=k) for k in kat],
           fontsize=7, loc="upper left", title="aktivna ograničenja")
ax2.set_title("Usko grlo")

for ax in (ax1, ax2):
    ax.set_xlabel("Drvo (m³)")
    ax.set_ylabel("Pakovanje (h)")
    ax.set_zlabel("Farbanje (h)")
    ax.plot([240], [100], [180], marker="*", color="k", ms=12)   # polazna tacka
    ax.view_init(elev=22, azim=-60)

fig.suptitle(f"Drvo, pakovanje i farbanje se menjaju zajedno (stolarija fiksirana na {STOLARIJA})")
plt.tight_layout()
plt.savefig("osetljivost3d.png", dpi=130)