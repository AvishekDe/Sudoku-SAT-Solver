import itertools
import os
import sys

puzzle = [
    "5***1***4",
    "***2*6***",
    "**8*9*6**",
    "*4*****1*",
    "7*1*8*4*6",
    "*5*****3*",
    "**6*4*1**",
    "***5*2***",
    "2***6***8"
]

clauses = []
digits = range(1,10)

def varnum(i,j,k):
    assert(i in digits and j in digits and k in digits)
    return 100*i+10*j+k

def exactly_one_of(literals):
    clauses.append([l for l in literals])

    for pair in itertools.combinations(literals,2):
        clauses.append([-l for l in pair])

def invoke_solver(name):
    if(name == "minisat"):
        os.system("minisat tmp.cnf minisat.sat > minisat_stats.out")
    elif(name == "z3"):
        os.system("z3 tmp.cnf > z3.sat")
    elif(name == "sat4j"):
        os.system("java -jar org.sat4j.core-2.3.1.jar tmp.cnf > sat4j.sat")
    elif(name == "all"):
        os.system("minisat tmp.cnf minisat.sat > minisat_stats.out")
        os.system("z3 tmp.cnf > z3.sat")
        os.system("java -jar org.sat4j.core-2.3.1.jar tmp.cnf > sat4j.sat")

def print_minisat():
    print("-------MINISAT Solver-------")
    with open("minisat.sat", "r") as satfile:
        for line in satfile:
            if line.split()[0] == "UNSAT":
                print("UNSAT")
            elif line.split()[0] == "SAT":
                print("SAT")
            else:
                assignment = [int(x) for x in line.split()]

                for i in digits:
                    for j in digits:
                        for k in digits:
                            if(varnum(i,j,k) in assignment):
                                print(k, end="")
                                break
                    print("")

def print_z3():
    print("-------Z3 Solver-------")
    with open("z3.sat", "r") as satfile:
        for line in satfile:
            if line.split()[0] == "s" and line.split()[1] == "UNSATISFIABLE":
                print("UNSAT")
            elif line.split()[0] == "s" and line.split()[1] == "SATISFIABLE":
                print("SAT")
            else:
                assignment = [int(x) for x in line.split()[1:]]

                for i in digits:
                    for j in digits:
                        for k in digits:
                            if(varnum(i,j,k) in assignment):
                                print(k, end="")
                                break
                    print("")

def print_sat4j():
    print("-------SAT4J Solver-------")
    with open("sat4j.sat", "r") as satfile:
        for line in satfile:
            if(line.split()[0] == "c"):
                pass
            elif line.split()[0] == "s" and line.split()[1] == "UNSATISFIABLE":
                print("UNSAT")
            elif line.split()[0] == "s" and line.split()[1] == "SATISFIABLE":
                print("SAT")
            else:
                assignment = [int(x) for x in line.split()[1:]]

                for i in digits:
                    for j in digits:
                        for k in digits:
                            if(varnum(i,j,k) in assignment):
                                print(k, end="")
                                break
                    print("")

def print_results(name):
    if(name == "minisat"):
        print_minisat()
    elif(name == "z3"):
        print_z3()
    elif(name == "sat4j"):
        print_sat4j()
    elif(name == "all"):
        print_minisat()
        print_z3()
        print_sat4j()

# cell (i,j) contains exactly 1 digit
for(i,j) in itertools.product(digits, repeat=2):
    exactly_one_of([varnum(i,j,k) for k in digits])

# k appears exactly once in row i
for(i,k) in itertools.product(digits, repeat=2):
    exactly_one_of([varnum(i,j,k) for j in digits])

# k appears exactly once in column j
for(j,k) in itertools.product(digits, repeat=2):
    exactly_one_of([varnum(i,j,k) for i in digits])

# k appears exactly once in mini-grid
for(i,j) in itertools.product([1,4,7], repeat=2):
    for k in digits:
        exactly_one_of([varnum(i+deltai,j+deltaj,k) for (deltai,deltaj) in itertools.product(range(3), repeat=2)])

for(i,j) in itertools.product(digits, repeat=2):
    if puzzle[i-1][j-1]!="*":
        k = int(puzzle[i-1][j-1])
        assert(k in digits)
        # i,j already contains k
        clauses.append([varnum(i,j,k)])

with open("tmp.cnf", "w") as f:
    f.write("p cnf {} {}\n".format(999, len(clauses)))
    for c in clauses:
        c.append(0);
        f.write(" ".join(map(str,c))+"\n")


# check which solver we are using
solver_name_input = sys.argv[1]

invoke_solver(solver_name_input)
print_results(solver_name_input)