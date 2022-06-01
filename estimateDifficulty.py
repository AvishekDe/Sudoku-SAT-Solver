import os
import time

csv = "solver,diff,file,duration\n"

for solver in ["minisat"]:
    for dir in os.listdir("./Puzzles"):
        if(dir.startswith("diff")):
            for file in os.listdir("./Puzzles/"+dir):
                start = time.time()
                os.system("python3 solver.py solve "+solver+" "+dir+"/"+file)
                end = time.time()
                duration = end - start
                csv += solver+","+dir+","+file+","+str(duration)+"\n"

with open("resultsDiff.csv","w") as c:
    c.write(csv)