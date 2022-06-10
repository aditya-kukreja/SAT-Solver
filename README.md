# SAT-Solver
Implementation of a SAT solving algorithm, Davis-Putnam-Logemann-Loveland (DPLL) which solves the NP-complete SAT problem by simple backtracking along with a few pruning techniques. The input is a SAT formula in DIMACS format and the output is a single line "SAT" followed by space seperated assignments to the literals in a newline in case the formula is satisfied or else the output is just a single line "UNSAT". The SAT Solver is then used to solve a Sudoku puzzle that is generated and converted to the conjuctive normal form.
