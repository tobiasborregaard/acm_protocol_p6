import os

directory = "data/"
files = os.listdir(directory)


with open("output.csv", 'w') as f:
    for index, i in enumerate(sorted(files)):
        if index % 2 == 0 or index % 2 ==1:
            with open(directory + i, 'r') as data:
                for lineindex, line in enumerate(data.readlines()):
                    if index != 0 and lineindex == 0:
                        pass
                    elif line.endswith(",0\n"):
                        pass
                    else:
                        f.write(line)

