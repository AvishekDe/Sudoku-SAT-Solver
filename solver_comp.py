import os
import time

csv = "solver,file,duration\n"

for solver in ["minisat","sat4j","z3"]:
    for dir in os.listdir("./Puzzles"):
        if(dir.startswith("Grid")):
            #for file in os.listdir("./Puzzles/"+dir):
                start = time.time()
                os.system("python3 solver.py solve "+solver+" "+dir)
                end = time.time()
                duration = end - start
                csv += solver+","+dir+","+str(duration)+"\n"

with open("compareresultsDiff.csv","w") as c:
    c.write(csv)