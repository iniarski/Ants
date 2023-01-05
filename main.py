import ant
import time
import filemaker

def main():
    data = ant.Anthill("TSP.txt")

    path0 = data.basic()
    path1 = data.greedy(0)
    path2 = data.ants(0)

    print(data.pathLen(path0), data.pathLen(path1), data.pathLen(path2))



    # time complexity with reference of number of nodes

    nodes = 10

    basicTimes = []
    greedyTimes = []
    antTimes = []
    basicPaths = []
    greedyPaths = []
    antPaths = []

    for i in range(8):
        filemaker.mkfile('nodes.txt', nodes)

        data = ant.Anthill('nodes.txt')

        start = time.time()

        basicPaths.append(data.pathLen(data.basic()))

        basicTimes.append(time.time() - start)

        start = time.time()

        greedyPaths.append(data.pathLen(data.greedy(0)))
        greedyTimes.append(time.time() - start)

        start = time.time()

        antPaths.append(data.pathLen(data.ants(0)))
        antTimes.append(time.time() - start)

        nodes *= 2

        print('Basic')
        print(basicPaths)
        print(basicTimes)

        print('Greedy')
        print(greedyPaths)
        print(greedyTimes)

        print('Ants')
        print(antPaths)
        print(antTimes)


if __name__ == '__main__':
    main()