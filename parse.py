download = open("download.txt","r")
lines = download.readlines()
currentfile= ""
count = -1
sudoku = ""

for line in lines:
    if line.startswith("Grid"):
        currentfile = "./Puzzles/"+line.replace(" ","_")
        count = 9
        sudoku = ""
    else:
        sudoku += line.replace("0","*")
        count-=1
        if count == 0:
            with open(currentfile,"w") as f:
                f.write(sudoku)

    