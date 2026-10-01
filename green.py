import numpy as np
from scipy.optimize import linprog

hours = 24


price_grid = [
    5,
    5,
    4,
    4,
    5,
    6,
    9,
    14,
    18,
    18,
    16,
    14,
    12,
    12,
    14,
    17,
    22,
    25,
    20,
    15,
    11,
    8,
    6,
    5,
]
cost_battery = [0.0] * hours  # 

c = np.array(price_grid + cost_battery) 

demands = np.array([
    100,
    90,
    80,
    80,
    90,
    110,
    150,
    220,
    280,
    300,
    290,
    270,
    250,
    250,
    270,
    310,
    350,
    380,
    320,
    260,
    210,
    160,
    130,
    110,
])

A_demand = np.hstack([-np.eye(hours), -np.eye(hours)])
b_demand = -demands

A_batt_max = np.hstack([np.zeros((hours, hours)), np.eye(hours)])
b_batt_max = np.full(hours, 100)

A_ub = np.vstack([A_demand, A_batt_max])
b_ub = np.hstack([b_demand, b_batt_max])

bounds = [(0, None) for _ in range(2 * hours)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

if res.success:
  print('Optimalna strategija za 24 sata uspešno izračunata!')
  print(f'--------------------------------------------------')
  print(f'Ukupni minimalni trošak struje za dan: {res.fun:.2f} dinara\n')

  grid_used = res.x[:hours]
  battery_used = res.x[hours:]

  print(f'Sat\tZahtev\tIz Mreže\tIz Baterije')
  print(f'-----------------------------------------')
  for h in range(hours):
    print(
        f'{h:02d}:00\t{demands[h]} kW\t{grid_used[h]:.1f} kW\t\t'
        f'{battery_used[h]:.1f} kW'
    )
else:
  print('Optimizacija nije uspela.')