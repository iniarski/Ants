import random
import math


class Anthill:

    def dist(self, i, j):

        x = self.cities[i][0] - self.cities[j][0]
        y = self.cities[i][1] - self.cities[j][1]

        return math.sqrt(x * x + y * y)

    def __init__(self, sourceFile):

    # reading data from file

        with open(sourceFile) as file:
            content = file.read()
            content = content.splitlines()
            file.close()

        self.cityNum = len(content)
        self.cities = []

        for i in range(self.cityNum):
            line = content[i]
            line = line.split('\t')

            city = [float(line[1]), float(line[2])]

            self.cities.append(city)

    # calculating distances

        self.distances = []

        for i in range(self.cityNum):
            city = []

            for j in range(self.cityNum):
                city.append(self.dist(i, j))

            self.distances.append(city)

    # defining ant colony algorithm parameters
    # to be fiddled with

    # the strength of feromone the ants leave
    # here it's 1 over 10000 time the length of the path greedy algorithm found
        self.feromone = 1 / 13750000
    # keep distBias positive
    # else ants will try to find longest path
        self.distBias = 32
    # feromone bias determines how ants performance is evaluated
        self.feromoneBias = 168
    # numbers of iteration of the algorithm
        self.generation = 25
    # ants sent a generation
        self.antPerGen = 35

    def basic(self):
        path = [* range(self.cityNum)]
        path.append(0)
        return path

    def greedy(self, start):
        route = [start]

        visited = [start]
        unvisited = []

        for i in range(self.cityNum):
            unvisited.append(i)

        unvisited.pop(start)

        last = start

        while bool(unvisited):
            min = 999999999

            for i in range(len(unvisited)):
                if self.distances[last][unvisited[i]] < min:
                    next = i
                    min = self.distances[last][unvisited[i]]

            visited.append(unvisited.pop(next))

        visited.append(start)

        return visited

    def pathLen(self, path):
        length = 0
        for i in range(self.cityNum):
            length += self.distances[path[i]][path[i+1]]

        return length

    def ants(self, start):

    # creating table with ants preferneces
        biasTable = []

        for i in range(self.cityNum):
            biasLine = [0] * self.cityNum
            for j in range(i):
                biasLine[j] = 1 / math.pow(self.distances[i][j], self.distBias)
            for j in range(i + 1, self.cityNum):
                biasLine[j] = 1 / math.pow(self.distances[i][j], self.distBias)
            biasTable.append(biasLine)

    # making the ants find path

        shortestPath = self.basic()

        for gen in range(self.generation):
            pathList = []
            last = start

            for ant in range(self.antPerGen):
                visited = [start]
                unnvisted = [*range(self.cityNum)]

                unnvisted.pop(start)

                while bool(unnvisted):
                    biasList = []

    # ant chooses where to go

                    for i in range(len(unnvisted)):
                        biasList.append(biasTable[last][unnvisted[i]])

                    last = random.choices(unnvisted, biasList)[0]
                    lastIndex = unnvisted.index(last)


                    visited.append(unnvisted.pop(lastIndex))

                visited.append(start)
                pathList.append(visited)

    # evaluating paths and assigning feromone

            lengthList = []

            for k in range(self.antPerGen):
                lengthList.append(self.pathLen(pathList[k]))

            avLength = sum(lengthList) / self.antPerGen



    # performanceList stores how well an ant did compared to others in her generation

            performanceList = []

            for k in range(self.antPerGen):
                performanceList.append(math.pow(1 / lengthList[k], self.feromoneBias))

    # applying feromone to the biasTable
    # later generations of ants have stronger feromone

            for k in range(self.antPerGen):
                path = pathList[k]
                for l in range(self.cityNum):
                    biasTable[path[l]][path[l+1]] += self.feromone * performanceList[k] * (gen + 1)

            minIndex = performanceList.index(min(performanceList))

            if self.pathLen(pathList[minIndex]) < self.pathLen(shortestPath):
                shortestPath = pathList[minIndex]

        return shortestPath