import numpy as np
from scipy.optimize import linprog


#REŠENJE/POSTAVKA PROBLEMA OPTIMIZACIJE ZA 3 SATA (AI)
# 1. DEFINIŠEMO PROBLEM ZA 3 SATA (da bude pregledno, mada može za svih 24)
# Promenljive x u našem vektoru:
# [Struja_iz_mreže_sat1, Struja_iz_mreže_sat2, Struja_iz_mreže_sat3,
#  Baterija_sat1,       Baterija_sat2,       Baterija_sat3]
# Ukupno 6 promenljivih.

# 2. CILJNA FUNKCIJA (Troškovi po satima)
# Pretpostavimo da je cena struje iz mreže ujutro jeftina (5 din), podne skupa (15 din), uveče srednja (10 din).
# Baterija nema direktnu cenu nabavke struje, njen trošak je 0.
c = np.array([5.0, 15.0, 10.0, 0.0, 0.0, 0.0])

# 3. OGRANIČENJA U OBLIKU MATRICA (A_ub * x <= b_ub)
# Zahtevana energija koju serveri MORAJU da dobiju u sat 1, 2 i 3: [100 kW, 200 kW, 150 kW]
# Energija iz mreže + Energija iz baterije >= Zahtevana energija
# Prevedeno u standardni oblik (<=): -(Mreža + Baterija) <= -Zahtev

demands = np.array([100, 200, 150])

# Matrica A_ub (dimenzije: broj ograničenja x broj promenljivih)
# Prateći uslove za balans energije i kapacitet baterije:
A_ub = np.array([
    # Sat 1: Mreža + Baterija >= 100  -->  -Mreža1 - Bat1 <= -100
    [-1, 0, 0, -1, 0, 0],
    # Sat 2: Mreža + Baterija >= 200  -->  -Mreža2 - Bat2 <= -200
    [0, -1, 0, 0, -1, 0],
    # Sat 3: Mreža + Baterija >= 150  -->  -Mreža3 - Bat3 <= -150
    [0, 0, -1, 0, 0, -1],
    # Ograničenje kapaciteta baterije (ne može da isprazni više od 80 kW u cugu)
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1],
])

b_ub = np.array([
    -100,  # Minimalna energija sat 1
    -200,  # Minimalna energija sat 2
    -150,  # Minimalna energija sat 3
    80,  # Max pražnjenje baterije sat 1
    80,  # Max pražnjenje baterije sat 2
    80,  # Max pražnjenje baterije sat 3
])

# Granice promenljivih (sve moraju biti >= 0)
bounds = [(0, None) for _ in range(6)]

# 4. REŠAVANJE MATRIČNOG SISTEMA PREKO SCIPY LINPROG
res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

if res.success:
  print('Matrični sistem uspešno rešen!')
  print(f'-----------------------------------')
  print(f'Optimalne vrednosti promenljivih (x): {np.round(res.x, 2)}')
  print(f'Ukupni minimalni trošak električne energije: {res.fun:.2f} dinara')
else:
  print('Optimizacija nije uspela.')