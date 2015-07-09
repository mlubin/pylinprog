# pylinprog
This is a proof-of-concept implementation of the ``linprog`` function in python. If you find it useful, please submit a PR to help document it and turn it into a real Python package.

## Wait, doesn't scipy have [linprog](http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.optimize.linprog.html)?

Yes it does, but it currently only provides a textbook implementation of the *dense* simplex algorithm, capable of up to thousands of variables and constraints. Most linear programming problems in practice are highly sparse and may have millions of variables and constraints. This ``linprog`` implementation exposes state-of-the-art open-source and commercial solvers.

## How does it work?

The implementation provides a thin wrapper around the [MathProgBase](https://github.com/JuliaOpt/MathProgBase.jl) library in Julia which provides links to [tons](http://www.juliaopt.org/) of solvers. Consequently, to use pylinprog, you need to have an installation of Julia and the experimental [pyjulia](https://github.com/JuliaLang/pyjulia) package.

## How do I use it?

The signature of ``linprog`` mostly matches that of scipy's [linprog](http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.optimize.linprog.html), with a special ``solver`` parameter to let you switch solvers. Scipy sparse matrices are accepted as coefficient matrices. See ``example.py``.
