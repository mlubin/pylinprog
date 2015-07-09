import numpy as np
from scipy.sparse import csr_matrix, csc_matrix, vstack 
import julia
j = julia.Julia()
j.call("using MathProgBase")
from julia import MathProgBase

def solver(packagename,solvername):
    j.call("using %s" % packagename)
    return j.eval(solvername)

clp = solver("Clp","ClpSolver()")


linprog_wrapper = j.eval("""
function lp_wrapper(c, sense, b, l, u, solver, m, n, colptr, rowval, nzval)
    @assert length(c) == length(l) == length(u) == n
    @assert length(b) == length(sense) == m
    
    sense_chr = Char[s[1] for s in sense]
    A = SparseMatrixCSC(m,n,colptr+1,rowval+1,nzval)
    sol = linprog(c,A,sense_chr,b,l,u,solver)
    return sol.status, sol.objval, sol.sol
end
""")


#Minimize: c^T * x
#
#Subject to: A_ub * x <= b_ub
#A_eq * x == b_eq
def linprog(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None, solver=None):
    if solver == None:
        solver = clp
    n = len(c)
    c = np.array(c)
    if A_ub == None:
        A_ub = csr_matrix((0,n))
        b_ub = np.array([])
    else:
        A_ub = csr_matrix(A_ub)
    if A_eq == None:
        A_eq = csr_matrix((0,n))
        b_eq = np.array([])
    else:
        A_eq = csr_matrix(A_eq)
    if bounds == None:
        bounds = [(0,None)]
    if len(bounds) == 1: # expand out
        bounds = [bounds[0] for i in range(n)]
    l = np.zeros(n)
    u = np.zeros(n)
    for k in range(len(bounds)): # convert None to Inf
        lower,upper = bounds[k]
        if lower == None:
            l[k] = float('-inf')
        else:
            l[k] = lower
        if upper == None:
            u[k] = float('inf')
        else:
            u[k] = upper
    senses = ['<' for i in range(len(b_ub))] + ['=' for i in range(len(b_eq))]
    A = vstack([A_ub,A_eq]).tocsc()
    assert(A.has_sorted_indices)
    b = np.hstack([b_ub,b_eq])
    m = len(b)

    return linprog_wrapper(c,senses,b,l,u,solver,m,n,A.indptr,A.indices,A.data)
