from copy import deepcopy
import queue
import re
from random import random


class Graph:
    Gr = dict(dict())
    dtype = str
    Weighted = True
    Directed = True

    def __init__(self, graph_dict, directed, weighted):
        self.Gr = deepcopy(graph_dict)
        self.Directed = directed
        self.Weighted = weighted

    @classmethod
    def createFromFile(cls, path):
        with open(path) as f:
            temp = dict(dict())
            Weighted, Directed = f.readline().upper().split()
            Weighted = (Weighted == "WEIGHTED" or Weighted == "YES")
            Directed = (Directed == "DIRECTED" or Directed == "YES")
            for line in f:
                listOfVertices = list(filter(None, re.split(':|,| |\n', line)))
                if Weighted:
                    temp[listOfVertices[0]] = dict(zip(listOfVertices[1::2], [float(x) for x in listOfVertices[2::2]]))
                else:
                    temp[listOfVertices[0]] = dict(zip(listOfVertices[1:], [1.] * len(listOfVertices[1:])))
        return cls(temp, Directed, Weighted)
    @classmethod
    def createfromconsol(cls, n):
        temp = dict(dict())
        Weighted, Directed = input().upper().split()
        Weighted = (Weighted == "WEIGHTED" or Weighted == "YES")
        Directed = (Directed == "DIRECTED" or Directed == "YES")
        for i in range(n):
            listOfVertices = list(filter(None, re.split(':|,| ', input())))
            if Weighted:
                temp[listOfVertices[0]] = dict(zip(listOfVertices[1::2], [float(x) for x in listOfVertices[2::2]]))
            else:
                temp[listOfVertices[0]] = dict(zip(listOfVertices[1:], [1.] * len(listOfVertices[1:])))

        return cls(temp, Directed, Weighted)

    @classmethod
    def create_copy(cls, other):
        return cls(other.Gr, other.Directed, other.Weighted)

    @classmethod
    def createGrWoutLeaves(cls, graph):
        temp = cls.create_copy(graph)
        if temp == None:
            return None
        if temp.Directed:
            return temp

        lvs = [x for x in temp.Gr.keys() if len(temp.Gr[x]) == 1]
        for v in lvs:
            for to in temp.Gr[v].keys():
                temp.Gr[to].pop(v)
            temp.Gr.pop(v)
        return temp

    def write_to_txt(self, path):
        with open(path, 'w') as f:
            w = "Weighted"
            d = "Directed"
            if not self.Weighted:
                w = "Unweighted"
            if not self.Directed:
                d = "Undirected"
            f.write(w + " " + d + "\n")
            f.write(self.show())
            return True

    def show(self):
        if not self.Weighted:
            return '\n'.join([f"{x}: {', '.join([str(y) for y in self.Gr[x]])  }" for x in self.Gr])
        else:
            return '\n'.join([f"{x}: {', '.join([str(y) + ': ' + str(self.Gr[x][y]) for y in self.Gr[x]])  }" for x in self.Gr])

    def add_vertex(self, name):
        if self.Gr.get(name):
            raise KeyError("Vertex is already in the graph")
        self.Gr.setdefault(name, dict())

    def add_edge(self, v, to, w=1.):
        if not self.Gr.get(v) or not self.Gr.get(to):
            raise KeyError("Vertices are unknown to the graph")

        if v == to and not self.Directed:
            raise KeyError("V == To, impossible to perform, the graph is not directed")

        self.Gr[v][to] = w
        if not self.Directed:
            self.Gr[to][v] = w

    def remove_edge(self, v, to):
        if not self.Gr.get(v) or not self.Gr.get(v):
            raise KeyError("No matching vertices")

        if not self.Gr[v].get(to):
            raise KeyError("No matching edge")

        self.Gr[v].pop(to)
        if not self.Directed:
            self.Gr[to].pop(v)

    def remove_node(self, v):
        if not self.Gr.get(v):
            raise KeyError("Vertex is absent")
        self.Gr.pop(v)
        for from_v in self.Gr.keys():
            if v in self.Gr[from_v].keys():
                self.Gr[from_v].pop(v)

    def out_degree(self, name):
        if not self.Gr.get(name):
            raise KeyError("Vertex is not in the graph")
        return len(self.Gr[name])

    def remove_all_leaves(self):
        if self.Directed:
            raise KeyError("To delete all leaves graph has to be undirected")
        for v in self.Gr.keys():
            if len(v) == 1:
                self.remove_node(v)

    def DFS(self, checked, cur, cur_path, dest, result):
        if cur == dest:
            #print out the path here
            cur_path.append(cur)
            result.append(cur_path)
            return
        checked = deepcopy(checked)
        checked[cur] = True # creating deepcopies?
        cur_path = deepcopy(cur_path)
        cur_path.append(cur) # creating deepcopies?
        for v in self.Gr[cur].keys():
            if not checked[v]:
                self.DFS(checked, v, cur_path, dest, result)

    def find_all_paths_a(self, u, v):
        checked = dict.fromkeys(self.Gr.keys(), False)
        cur_path = []
        result = []
        self.DFS(checked, u, cur_path, v, result)
        return result

    def DFS_b(self, u, dest, path, result):
        if u == dest:
            path.append(dest)
            result.append(path)
            return
        path = deepcopy(path)
        path.append(u)
        for ver in self.Gr[u].keys():
            temp = Graph.create_copy(self)
            temp.remove_edge(u, ver)
            temp.DFS_b(ver, dest, path, result)

    def find_all_paths_b(self, u, v):
        result = []
        path = []
        self.DFS_b(u, v, path, result)
        return result

    def BFS(self,v):
        q = queue.Queue()
        q.put(v)
        INF = 1e9
        path = dict.fromkeys(self.Gr.keys(), INF)
        color = dict.fromkeys(self.Gr.keys(), 0)# 0 = white
        path[v] = 0
        color[v] = 1
        while not q.empty():
            k = q.get()

            for to in self.Gr[k]:
                if path[to] == INF:
                    path[to] = path[k] + 1
                    q.put(to)
        return path

    def find_shortest_loop(self):
        if not self.Directed or self.Weighted:
            raise KeyError("Graph has to be DIRECTED and UNWEIGHTED")
        res = {v:self.BFS(v) for v in self.Gr.keys()}
        return min([min([res[v][u] + res[u][v] for u in res[v].keys() if u != v]) for v in res.keys()])
    def prim(self, v):
        if v not in self.Gr.keys():
            raise KeyError("No such vertex")
        INF = 1e9
        used = dict.fromkeys(self.Gr.keys(), False)
        min_e = dict.fromkeys(self.Gr.keys(), INF)
        sel_e = dict.fromkeys(self.Gr.keys(), -1)

        min_e[v] = 0
        n = len(self.Gr.keys())
        for i in self.Gr.keys():
            v = None
            for j in self.Gr.keys():
                if not used[j] and (not v or min_e[j] < min_e[v]):
                    v = j
            if min_e == INF:
                raise KeyError("No MST")

            used[v] = True
            if sel_e[v] != -1:
                print(v, sel_e[v])
            for to in self.Gr[v].keys():
                if self.Gr[v][to] < min_e[to]:
                    min_e[to] = self.Gr[v][to]
                    sel_e[to] = v

    #Определить,
    # существует ли путь длиной не более L между двумя
    # заданными вершинами графа.
    def Dijkstra(self, u, v):
        INF = 1e9
        dist = dict.fromkeys(self.Gr.keys(), INF)
        used = dict.fromkeys(self.Gr.keys(), False)
        prev = dict.fromkeys(self.Gr.keys(), 0)
        dist[u] = 0
        for i in self.Gr.keys():
            v = None
            min_d = INF
            for j in self.Gr.keys():
                if dist[j] < min_d and not used[j]:
                    min_d = dist[j]
                    v = j
            used[v] = True
            for j in self.Gr[v].keys():
                if dist[j] > min_d + self.Gr[v][j]:
                    dist[j] = min_d + self.Gr[v][j]
                    prev[j] = v
        return dist
    def find_all_in_range(self, u, v, L):
        dist = self.Dijkstra(u,v)

        return {x:dist[x] for x in dist.keys() if dist[x] <= L}

    def exists_path(self, u, v, L):
        if u not in self.Gr.keys() or v not in self.Gr.keys():
            raise KeyError("Vertices are absent")
        return v in self.find_all_in_range(u, v, L).keys()

    #Вывести кратчайшие пути из вершин u1 и u2 до v.
    def Floyd(self):
        INF = 1e9
        dist = deepcopy(self.Gr)
        prev = dict()
        for v in self.Gr:
            prev[v] = dict.fromkeys(self.Gr.keys(), -1)
            for w in self.Gr:

                if not dist[v].get(w):
                    if v == w:
                        dist[v][w] = 0
                    else:
                        dist[v][w] = INF
        for k in self.Gr.keys():
            for i in self.Gr.keys():
                for j in self.Gr.keys():
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        prev[i][j] = k
        return prev
    #Вывести кратчайшие пути из вершин u1 и u2 до v.
    def show_shortest_(self, u1, u2, v):
        prev = self.Floyd()
        print("first")
        print(u1)
        self.get_revpath(prev, u1, v)
        print(v)
        print("second")
        print(u2)
        self.get_revpath(prev, u2, v)
        print(v)

    def get_revpath(self, prev, u, v):
        cur = prev[u][v]
        if cur != -1:
            self.get_revpath(prev, u, cur)
            print(cur)
            self.get_revpath(prev, cur, v)

    def Bellman(self, s):
        #работает на отриц ребрах, детектит отриц циклы

        INF = 1e9 + max([max([self.Gr[x][y] for y in self.Gr[x].keys()]) for x in self.Gr.keys()])*len(self.Gr.keys())
        dist = dict.fromkeys(self.Gr.keys(), INF)
        dist[s] = 0
        for i in range(len(self.Gr.keys())):
            flag = False
            for x in self.Gr.keys():
                for y in self.Gr[x].keys():
                    if dist[x] > dist[y] + self.Gr[y][x]:
                        dist[x] = dist[y] + self.Gr[y][x]
                        flag = True
            if not flag:
                break
            if i == len(self.Gr.keys())-1 and flag:
                raise KeyError("Negative circle was found")
        return dist
    def N_peref(self, u, N):
        dist = self.Bellman(u)
        return {x:dist[x] for x in dist.keys() if dist[x]>N}
    #N-периферией для вершины называется множество вершин,
# расстояние от которых до заданной вершины больше N.
# Определить N-периферию для заданной вершины графа.





