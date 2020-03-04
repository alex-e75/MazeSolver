import operator
import random
from colorama import Fore,Style

class MazeSolver:
    def __init__(self, lines, columns):
        self.__lines = lines
        self.__columns = columns
        self.__block = '|'
        self.__freePath = '0'
        self.__minorPath = 'x'
        self.__matrix = self.CreateMatrix()
        self.INFINITY = float('inf')
        self.__dist = dict()
        self.__parent = dict()
        #Using dict comprehension
        #self.__dist = {(element,item): self.INFINITY for element in range(len(matrix)) for item in range(len(matrix[0]))}
        for element in range(self.__lines):
            for item in range(self.__columns):
                self.__dist[(element,item)] = self.INFINITY
                self.__parent[(element,item)] = self.INFINITY

    def Djikstra(self,vStart):
        self.__dist[vStart] = 0
        self.__parent[vStart] = vStart
        quee = [vStart+(0,)]

        while(quee):
            popped = quee.pop(0)[0:2]
            neighbours = self.GetNeighbours(popped[0],popped[1])
            for element in neighbours:
                dist = element[2]+self.__dist[popped]
                if dist < self.__dist[element[0:2]]:
                    quee.append(element)
                    self.__parent[element[0:2]] = popped
                    self.__dist[element[0:2]] = dist
            quee.sort(key=operator.itemgetter(2))

    def DjikstraShotestPath(self,vStart,vEnd):
        self.CreateMaze(vStart)
        self.__matrix[vStart[0]][vStart[1]] = 'A'
        self.__matrix[vEnd[0]][vEnd[1]] = 'B'
        print('Objetivo: Chegar de A a B')
        self.PrintMatrix()
        self.Djikstra(vStart)

        if(self.__dist[vEnd] == self.INFINITY):
            print("Não existe caminho entre {} e {}.".format(vStart,vEnd))
        else:
            self.__matrix[vStart[0]][vStart[1]] = self.__minorPath
            shortestPath = [vEnd]
            parent = vEnd
            while(parent!=vStart):
                self.__matrix[parent[0]][parent[1]] = self.__minorPath
                parent = self.__parent[parent]
                shortestPath.insert(0,parent)
            print("Resultado:")
            self.PrintMatrix()
            print("A menor distância entre {} e {} é: {:.2f}".format(vStart,vEnd,self.__dist[vEnd]))
            print("O menor caminho é: {}".format(shortestPath))

    def GetNeighbours(self,line, column,excludeBlock=True):
        neighbours = []
        delta = [(0,1),(1,0),(-1,0),(0,-1)]
        for (x,y) in delta:
            if (line+x <= 0 or line+x >= len(self.__matrix) - 1 or column+y <= 0 or column+y >= len(self.__matrix[0]) - 1
                    or (self.__matrix[line+x][column+y] == self.__block and excludeBlock)):
                continue
            else:
                neighbours.append((line+x,column+y, 1))
        return neighbours

    def PrintMatrix(self):
        for i in range(len(self.__matrix)):
            for item in self.__matrix[i]:
                if(item==self.__minorPath):
                    print(Fore.YELLOW+""+item,end="")
                    print(Style.RESET_ALL+" ",end="")
                elif(item==self.__block):
                    print(Fore.RED + "" + item, end="")
                    print(Style.RESET_ALL + " ", end="")
                elif(item=='A' or item=='B'):
                    print(Fore.BLUE + "" + item, end="")
                    print(Style.RESET_ALL + " ", end="")
                else:
                    print(item+" ",end="")
            print('')

    def CreateMaze(self,vStart): #Using Kruskal
        maze = set()
        nodeStack = set()
        notValidNodes = set()
        currentNode = vStart
        nodeStack.add(currentNode)

        while(nodeStack):
            maze.add(currentNode)
            self.__matrix[currentNode[0]][currentNode[1]] = self.__freePath
            neighbours = self.GetNeighbours(currentNode[0],currentNode[1],False)
            neighbours = [(element[0],element[1]) for element in neighbours]
            neighbours = list(set(neighbours) - notValidNodes)
            while(True):
                if(not neighbours):
                    break
                found = True
                nextNode = random.choice(neighbours)
                nextNeighbours = self.GetNeighbours(nextNode[0],nextNode[1],False)
                for element in nextNeighbours:
                    if((element[0:2] in maze) and not(element[0:2] == currentNode)):
                        found = False
                if(found):
                    break
                else:
                    neighbours.remove(nextNode)

            if(found):
                nodeStack.add(currentNode)
                currentNode = nextNode[0:2]
            else:
                notValidNodes.add(currentNode)
                currentNode = nodeStack.pop()


    def CreateMatrix(self):
        return [['|'] * self.__columns for i in range(self.__lines)]


lines = 20
columns = 50

startNode = (2,3)
endNode = (5,47)

graph = MazeSolver(lines,columns)
graph.DjikstraShotestPath(startNode,endNode)