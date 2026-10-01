from ortools.sat.python import cp_model


def solve_optimization():
  model = cp_model.CpModel()

  tables = model.NewIntVar(0, 30, 'tables')
  chairs = model.NewIntVar(0, 30, 'chairs')

  
  model.Add(tables + chairs >= 15)

  model.Minimize(3 * tables + 2 * chairs)

  solver = cp_model.CpSolver()
  status = solver.Solve(model)

  if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print('Pronađeno optimalno rešenje!')
    print(f'-----------------------------------')
    print(f'Broj stolova: {solver.Value(tables)}')
    print(f'Broj stolica: {solver.Value(chairs)}')
    print(f'Minimalno utrošenih radnih sati: {solver.ObjectiveValue()}')
  else:
    print('Nije pronađeno rešenje – uslovi su kontradiktorni.')


if __name__ == '__main__':
  solve_optimization()