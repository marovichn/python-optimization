import numpy as np
from scipy.optimize import linprog

#Zadatak: Fabrika nameštaja

#Fabrika proizvodi stolove, stolice i police. Cilj je maksimizovati dnevni profit.

#	    Sto	      Stolica	    Polica	Raspoloživo
#Drvo (m³)	    3	1	2	240
#Stolarija (h)	4	2	3	360
#Farbanje (h)	2	1	2	180
#Pakovanje (h)	1	1	1	100
#Profit (€/kom)	120	70	90	

#Dodatna ograničenja:

#Ugovor obavezuje fabriku da proizvede najmanje 10 stolica.
#Tržište upija najviše 40 polica.
#Količine mogu biti razlomljene (to je LP, ne celobrojni problem)

#RESENJE

#ciljna funkcija: maksimizovati profit
# maximize: 120x1 + 70x2 + 90x3
#zbog linprog koja minimizira, koristimo negativne koeficijente

c= np.array([-120, -70, -90])


#Ograničenja: A_ub 

A_ub = np.array([
    [3, 1, 2],
    [4, 2, 3],
    [2, 1, 2],
    [1, 1, 1],
    [0, -1, 0],
    [0, 0, 1]])

#slobodni koeficijenti desne strane: b_ub
b_ub = np.array([240, 360, 180, 100, -10, 40])

#bounds: x1, x2, x3 >= 0 LP može imati slobodne promenljive (npr. višak/manjak, temperatura, razlika u zalihama) mi racunamo da su sve promenljive nenegativne bounds = (0, None)

# !!!! NAUCIO SAM DA za bolji rad solvera koji granice tretira efikasnije nego ogranicenja koristicemo poslednja dva reda iz A_ub i b_ub kao bounds, i izbaciti ih iz ogranicenja. Na taj nacin solver ce imati manje ogranicenja i brze ce pronaci optimalno resenje.

A_ub = np.array([
    [3, 1, 2],
    [4, 2, 3],
    [2, 1, 2],
    [1, 1, 1]])

b_ub = np.array([240, 360, 180, 100])

bounds = [(0, None), (50, None), (0, 40)]

#method za linprog koji cu koristiti je HiGHS

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

if res.success:
    print('Optimalna strategija za proizvodnju uspešno izračunata!')
    print(f'--------------------------------------------------')
    print(f'Ukupni maksimalni profit za dan: {-res.fun:.2f} €\n')

    x1, x2, x3 = res.x
    s1, s2, s3, s4 = res.slack

    print(f'Proizvedeno stolova: {x1:.2f}')
    print(f'Proizvedeno stolica: {x2:.2f}')
    print(f'Proizvedeno polica: {x3:.2f}')
    
    resursi = ["drvo", "stolarija", "farbanje", "pakovanje"]
    for ime, s in zip(resursi, res.slack):
        status = "AKTIVNO (usko grlo)" if np.isclose(s, 0) else "ima viška"
        print(f"{ime:<10} slack = {s:6.2f}  ->  {status}")

    print("shadow prices:", res.ineqlin.marginals)
    print("reducirani troškovi (donje granice):", res.lower.marginals)
    print("reducirani troškovi (gornje granice):", res.upper.marginals)
            
    print(f'-----------------------------------------')
else:
  print('Optimizacija nije uspela.')