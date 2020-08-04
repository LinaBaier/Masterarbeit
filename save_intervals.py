def save_intervals(name, intervals):
    intervals = intervals.split("Dimension: ")
    del intervals[0]
    i = 0
    while i < len(intervals):
        dim0 = intervals[i].split("\n")
        if i < len(intervals)-1:
            dim1 = intervals[i+1].split("\n")
            dim1 = dim1 if dim1[0] == "1" else ["",""]  
        else:
            dim1 = ["",""]
        if i < len(intervals)-2:
            dim2 = intervals[i+2].split("\n")
            dim2 = dim2 if dim2[0] == "2" else ["",""]
        else:
            dim2 =["",""]
        del dim0[0], dim0[-1], dim1[0], dim1[-1], dim2[0], dim2[-1]
        len0, len1, len2 = str(len(dim0)), str(len(dim1)), str(len(dim2))
        with open("Ergebnisse_test.csv","a") as file:
            file.write(name + ";" + str(dim0) + ";" + str(dim1) + ";" + str(dim2) + ";" + len0 + ";" + len1 + ";" + len2 + "\n")
        i += 3


      

'''
    for i in range(0, len(intervals),3):
        if i = len(intervals)-1:
            speiche
        elif intervals
        dim0, dim1, dim2 = intervals[i].split("\n"), intervals[i+1].split("\n"), intervals[i+2].split("\n")
        del dim0[0], dim1[0], dim2[0], dim0[-1], dim1[-1], dim2[-1]
        len0, len1, len2 = str(len(dim0)), str(len(dim1)), str(len(dim2))
        with open("Ergebnisse.csv","a") as file:
            file.write(name + ";" + str(dim0) + ";" + str(dim1) + ";" + str(dim2) + ";" + len0 + ";" + len1 + ";" + len2 + "\n")
'''