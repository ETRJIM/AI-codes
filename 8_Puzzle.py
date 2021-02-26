from collections import *
import heapq
import time
import os, psutil
process = psutil.Process(os.getpid())
print(process.memory_info().rss)
def Manhattan_distance(state):
    heuristic = 0

    for i in range(len(state)):
        X_distance = abs(int(i / 3) - int(int(state[i]) / 3))
        Y_distance = abs(int(i % 3) - int(int(state[i]) % 3))
        total_distance = X_distance + Y_distance
        heuristic += total_distance
    return heuristic
class puzzle:
#initiation of class puzzle
    def __init__(self,state,parent = None,move = "",depth = 0):
        self.state = state
        self.move = move
        self.parent = parent
        self.depth = depth
    def __str__(self):
        return self.state
#making the class orderable
    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.state < other.state

#generating next possible puzzles
    def child(self):
        childs = []
        childs.append(self.up())
        childs.append(self.down())
        childs.append(self.left())
        childs.append(self.right())
        return list(filter(None,childs))

#puzzle by up move
    def up(self):
        t = self.state.index('0')
        if t > 2:
            newstate = self.state[:t-3] + '0' + self.state[t-2:t] + self.state[t-3] + self.state[t+1:]
            upchild = puzzle(newstate,self,"U",self.depth + 1)
            return upchild
        else :
            return

#puzzle by down move
    def down(self):
        t = self.state.index('0')
        if t < 6:
            newstate = self.state[:t] + self.state[t + 3] + self.state[t + 1:t + 3] + '0' + self.state[t + 4:]
            downchild = puzzle(newstate,self,"D",self.depth + 1)
            return downchild
        else :
            return

#puzzle by left move
    def left(self):
        t = self.state.index('0')
        if t%3 != 0:
            newstate = self.state[:t - 1] + '0' + self.state[t - 1] + self.state[t + 1:]
            leftchild = puzzle(newstate,self,"L",self.depth + 1)
            return leftchild
        else :
            return

#puzzle by right move
    def right(self):
        t = self.state.index('0')
        if t%3 != 2:
            newstate = self.state[:t] + self.state[t + 1] + '0' + self.state[t + 2:]
            rightchild = puzzle(newstate,self,"R",self.depth + 1)
            return rightchild
        else :
            return
class solver:
    checked = set()
    check = set()
    checks = set()
    bfs_list = deque()
    dfs_list = deque()
    A_star_list = []
    count = 0
#initiating solver class
    def __init__(self,initial_puzzle,algo,goal_state = "123456780",count = 0):
        self.initial_puzzle = initial_puzzle
        self.goal_state = goal_state
        self.count = 0
        self.algo = algo
        if algo == "BFS":
            self.BFS()
        elif algo == "DFS":
            self.DFS()
        elif algo == "A_STAR":
            self.A_star()

#backtracing the path
    def journey(self,goal_puzzle):
        path = []
        nextgen = goal_puzzle

        while nextgen.state != self.initial_puzzle.state:
            path.append(nextgen.move)
            nextgen = nextgen.parent
        return path

#BFS
    def BFS(self):
        started = time.time()
        self.bfs_list.append(self.initial_puzzle)
        self.check.add(self.initial_puzzle.state)
        while len(self.bfs_list) > 0:
            current_puzzle = self.bfs_list.popleft()
            print(current_puzzle)
            if current_puzzle.state == self.goal_state:
                print("bfs solved this")
                v = self.journey(current_puzzle)
                print("depth: ",len(v))
                print(v[::-1])
                print("expanded nodes: ",self.count)

                break
            else:
                self.count += 1
                childs = current_puzzle.child()
                for child in childs:

                    if child.state not in self.check:
                        self.check.add(child.state)
                        self.bfs_list.append(child)
        else:
            print("No Solution")
            print("expanded nodes: ", self.count)
        print(str(time.time()-started))

#DFS
    def DFS(self):
        started = time.time()
        self.dfs_list.append(self.initial_puzzle)
        self.checked.add(self.initial_puzzle.state)
        while len(self.dfs_list) > 0:
            current_puzzle = self.dfs_list.pop()
            print(current_puzzle)
            if current_puzzle.state == self.goal_state:
                print("dfs solved this")
                v = self.journey(current_puzzle)
                print("depth: ", len(v))
                print(v[::-1])
                print("expanded nodes: ", self.count)
                break
            else:
                self.count += 1
                childs = current_puzzle.child()
                for child in childs:

                    if child.state not in self.checked:
                        self.checked.add(child.state)
                        self.dfs_list.append(child)
        else:
            print("No Solution")
            print("expanded nodes: ", self.count)
        print(str(time.time() - started))

#A_STAR
    def A_star(self):
        started = time.time()
        func = dict()
        self.A_star_list = []

        init_heuristic = Manhattan_distance(self.initial_puzzle.state)
        func[self.initial_puzzle.state] = init_heuristic
        self.checks.add(self.initial_puzzle.state)
        heapq.heappush(self.A_star_list, (func[self.initial_puzzle.state], self.initial_puzzle))
        while len(self.A_star_list) > 0:
            current_puzzle = heapq.heappop(self.A_star_list)[1]
            print(current_puzzle)
            if current_puzzle.state == self.goal_state:
                print("A_Star solved this")
                v = self.journey(current_puzzle)
                print("depth: ", len(v))
                print(v[::-1])
                print("expanded nodes: ", self.count)
                break
            else:
                self.count += 1
                childs = current_puzzle.child()
                for child in childs:
                    Manhattan = Manhattan_distance(child.state)
                    if child.state not in func.keys() or func[child.state] > Manhattan + child.depth:
                        func[child.state] = child.depth + Manhattan
                        heapq.heappush(self.A_star_list,(func[child.state], child))
        else:
            print("No Solution")
            print("expanded nodes: ", self.count)
        print(str(time.time() - started))
if __name__ == "__main__":
    print("input initial state")
    start = puzzle(input())
    print("which algo to use put the name in capital")
    solve = solver(start,input())
    process = psutil.Process(os.getpid())
    print("memory ",process.memory_info().rss, "Bytes")

#182043765
#523167480
#147258360 No solution