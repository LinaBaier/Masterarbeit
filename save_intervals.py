def save_intervals(name, intervals):
    intervals = intervals.split("Dimension: ")
    del intervals[0]
    i = 0
    while i < len(intervals):
        dim0 = intervals[i].split("\n")
        i += 1
        if i < len(intervals):
            dim1 = intervals[i].split("\n")
            if dim1[0] == "1":
                i += 1
            else:
                dim1 = ["",""]
        else:
            dim1 = ["",""]
        if i < len(intervals):
            dim2 = intervals[i].split("\n")
            if dim2[0] == "2":
                i += 1
            else:
                dim2 = ["",""]
        else:
            dim2 =["",""]
        del dim0[0], dim0[-1], dim1[0], dim1[-1], dim2[0], dim2[-1]
        with open("Ergebnisse_test.csv","a") as file:
            file.write(name + ";" + str(dim0) + ";" + str(dim1) + ";" + str(dim2) + "\n")