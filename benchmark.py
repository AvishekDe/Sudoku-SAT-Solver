import itertools
import os
import sys
import time
import pickle

mode = 'solve'
solver_name_input = 'all'

clauses = []
digits = range(1,10)

def exactly_one_of(literals):
    clauses.append([l for l in literals])

    for pair in itertools.combinations(literals,2):
        clauses.append([-l for l in pair])

def varnum(i,j,k):
    assert(i in digits and j in digits and k in digits)
    return 100*i+10*j+k
    
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

def load_puzzle(solution_filename, mode):
    solution = []

    if mode == 'solve':
        puzzle_filename = solution_filename
    else:
        solution_filepath = os.path.join('Solutions', solution_filename)
        with open(solution_filepath) as f:
            for line in f:
                solution.append(line.strip())
        puzzle_filename = solution[0]
        solution = solution[1:]

    puzzle_filepath = os.path.join('Puzzles', puzzle_filename)
    puzzle = []
    with open(puzzle_filepath, 'r') as f:
        for line in f:
            puzzle.append(line)
    return puzzle, solution  

def compare_solution(solution, answer):
    for i in range(len(solution)):
        if i%3 == 0 and i != 0:
            print('_'*44)
        for j in range(len(solution[0])):
            if j%3 == 0 and j != 0:
                print('| ', end='')
            if solution[i][j].isdigit() and solution[i][j] != answer[i][j]:
                print(f'{solution[i][j]}->{answer[i][j]}', end=' ')
            else:
                print(f'{solution[i][j]}   ', end=' ')
        print()

def systemcall(solver, command, timings):
    start = time.time()
    os.system(command)
    end = time.time()
    timings[solver] = end-start

def invoke_solver(name, timings):
    if(name == "minisat"):
        systemcall(name, "minisat tmp.cnf minisat.sat > minisat_stats.out", timings)
    elif(name == "z3"):
        systemcall(name, "z3 tmp.cnf > z3.sat", timings)
    elif(name == "sat4j"):
        systemcall(name, "java -jar org.sat4j.core-2.3.1.jar tmp.cnf > sat4j.sat", timings)
    elif(name == "all"):
        systemcall("minisat", "minisat tmp.cnf minisat.sat > minisat_stats.out", timings)
        systemcall("z3", "z3 tmp.cnf > z3.sat")
        systemcall("sat4j", "java -jar org.sat4j.core-2.3.1.jar tmp.cnf > sat4j.sat", timings)

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

def benchmark_puzzles(path):
    timings = {}
    puzzle, _ = load_puzzle(path, mode)
    invoke_solver(solver_name_input, timings)
    print(timings)
    return timings


if __name__ == '__main__':
    all_timings = {}
    for filename in os.listdir('Puzzles'):
        puzzle_path = os.path.join('Puzzles', filename)
        if os.path.isfile(puzzle_path):
            all_timings[filename] = benchmark_puzzles(filename)

    print(all_timings)
    pickle.dump('timings')            

    