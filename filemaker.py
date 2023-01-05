import random
import os

def mkfile(filename, cities):
    with open(filename, 'w') as file:
        for i in range(cities):
            line = str(i)
            line += '\t' + str(100 * random.random())
            line += '\t' + str(100 * random.random()) + '\n'

            file.write(line)

        file.close()

def rmfile(filename):
    os.remove(filename)