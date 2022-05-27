import os
import time

csv = "solver,file,duration\n"

for solver in ["minisat", "sat4j", "z3"]:
    for file in os.listdir("./Puzzles"):
        start = time.time()
        os.system("python3 solver.py solve "+solver+" "+file)
        end = time.time()
        duration = end - start
        csv += solver+","+file+","+str(duration)+"\n"

with open("results.csv","w") as c:
    c.write(csv)