 def save_intervals(name, intervals):
    name = "img2000"
    intervals = intervals.split("Dimension: ")
    del intervals[0]
    for i in range(0, len(intervals), 3):
        dim0, dim1, dim2 = intervals[i].split("\n"), intervals[i+1].split("\n"), intervals[i+2].split("\n")
        del dim0[0], dim1[0], dim2[0]
        len0, len1, len2 = str(len(dim0)), str(len(dim1)), str(len(dim2))
        with open("Ergebnisse_Morph.csv","a") as file:
            file.write(name + ";" + str(dim0) + ";" + str(dim1) + ";" + str(dim2) + len0 + len1 + len2 + "\n")


    
    col = "Dim " + str(i%3)
