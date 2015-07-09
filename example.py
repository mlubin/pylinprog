from pylinprog import linprog, solver

# minimize   -x
# subject to 2x + y <= 1.5
#            x,y >= 0

status, objval, sol = linprog([-1,0],A_ub=[[2,1]],b_ub = [1.5])

# using the commercial Gurobi solver (must have Gurobi license and Gurobi.jl package installed)
gurobi = solver("Gurobi", "GurobiSolver()")
status, objval, sol = linprog([-1,0],A_ub=[[2,1]],b_ub = [1.5], solver=gurobi)

