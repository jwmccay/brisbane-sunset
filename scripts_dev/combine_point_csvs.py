"""
Quickly combine some CSVs
"""

fnames = ["Home.csv", "Mission Blue.csv", "Library.csv"]

loc_list = []

for fname in fnames:
    with open(fname, "r") as f:
        lines = f.readlines()

    time_list = []
    date_list = []
    for line in lines:
        # Get column 1 and drop the newline
        time = line.split(",")[1][:-1]
        time_list.append(time)
        date = line.split(",")[0]
        date_list.append(date)
    loc_list.append(time_list)

new_lines = []
for i in range(len(loc_list[0])):
    new_line = f"{date_list[i]}"
    for j in range(len(loc_list)):
        new_line += f",{loc_list[j][i]}"
    new_line += "\n"
    new_lines.append(new_line)

with open("combined_csvs.csv", "w") as cc:
    cc.writelines(new_lines)
