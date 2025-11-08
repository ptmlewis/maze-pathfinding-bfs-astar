# first two lines are nxm dimensions
# N = empty cell
# W = Wall
# S = starting point
# G = goal point

from collections import deque
import heapq

maze = []

fileOpen = open("/Users/peterlewis/Desktop/VSCODE/PYTHON/Intelligent Systems/Assignment/Test Files/input.txt", "r");

m = int(fileOpen.readline().strip())
n = int(fileOpen.readline().strip())

for line in fileOpen:
    row = list(line.strip())
    for char in row:
        if char not in ['S', 'G', 'N', 'W', ' ']:
            print(f"Invalid character '{char}' found in the maze. Please use 'S' for the starting point, 'G' for the goal point, 'N' for empty cells, and 'W' for walls.")
            exit()
    maze.append(row)

fileOpen.close()

maze = [[char for char in row if char != ' '] for row in maze]

if 'S' not in ''.join([''.join(row) for row in maze]):
    print("No starting point 'S' found in the maze.")
    exit()

if 'G' not in ''.join([''.join(row) for row in maze]):
    print("No goal point 'G' found in the maze.")
    exit()

for m, row in enumerate(maze):
    for n, cell in enumerate(row):
        if cell == 'S':
            startingPoint = [m,n]
    
startingX, startingY = startingPoint

for m, row in enumerate(maze):
    for n, cell in enumerate(row):
        if cell == 'G':
            goalPoint = [m,n]

goal_x,goal_y = goalPoint

def valid_move_bfs(maze,start_x,start_y):

    rows,cols = m+1,n+1
    queue = deque([(start_x,start_y)])
    visited = set()
    previousVisitors = {}

    print("\nBreadth First Search (BFS)")
    print("Original Maze:")
    for row in maze:
        print(' '.join(row))

    while queue:
        x,y = queue.popleft()
        if (x,y) in visited:
            continue

        if maze[x][y] == 'G':
            path = []
            current = (x,y)
            
            while current !=(start_x,start_y):
                path.append(current)
                current = previousVisitors[current]
            path.append((start_x,start_y))
            path.reverse()            
            
            moves = []
            for i in range(1, len(path)):
                prev_x, prev_y = path[i - 1]
                curr_x, curr_y = path[i]
                if curr_x > prev_x:
                    moves.append('D')
                elif curr_x < prev_x:
                    moves.append('U')
                elif curr_y > prev_y:
                    moves.append('R')
                elif curr_y < prev_y:
                    moves.append('L')
            print("Sequence of moves:", '-'.join(moves))
            print("Total Path Length:",len(moves))
            print("Total Explored States:",len(visited))
            print("Total Path Cost:",len(moves)*10)

            print("Route taken:")
            for cell in path:
                 if maze[cell[0]][cell[1]] not in ['S', 'G']:
                    maze[cell[0]][cell[1]] = 'P'
            for row in maze:
                print(' '.join(row))
            return
    
        visited.add((x,y))

        for dx,dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and maze[new_x][new_y] != 'W' and (new_x,new_y) not in visited:
                queue.append((new_x, new_y))
                previousVisitors[(new_x,new_y)] = (x,y)
    
    print("BFS: No solution found")

valid_move_bfs(maze, startingX, startingY)

def heuristic(x, y, goal_x, goal_y):
    return abs(goal_x - x) + abs(goal_y - y)

def valid_move_astar(m, n, maze, startingX, startingY, goal_x, goal_y):
    row,cols = m+1,n+1
    start_cost = 0
    start_heuristic = heuristic(startingX,startingY,goal_x,goal_y)
    start_priority = start_cost + start_heuristic

    priority_queue = [(start_priority,start_cost,startingX,startingY)]
    heapq.heapify(priority_queue)
    visited = set()
    previous_visitors = {}

    while priority_queue:
        _, cost, x, y = heapq.heappop(priority_queue)
        if (x, y) in visited:
            continue

        if maze[x][y] == 'G':
            path = []
            current = (x, y)
            
            while current != (startingX, startingY):
                path.append(current)
                current = previous_visitors[current]
            path.append((startingX, startingY))
            path.reverse()
            
            moves = []
            for i in range(1, len(path)):
                prev_x, prev_y = path[i - 1]
                curr_x, curr_y = path[i]
                if curr_x > prev_x:
                    moves.append('D')
                elif curr_x < prev_x:
                    moves.append('U')
                elif curr_y > prev_y:
                    moves.append('R')
                elif curr_y < prev_y:
                    moves.append('L')
            print("\nA* Search")
            print("Original Maze:")
            for row in maze:
                print(' '.join(row))
            print("Sequence of moves:", '-'.join(moves))
            print("Total Path Length:", len(moves))
            print("Total Explored States:", len(visited))
            print("Total Path Cost:", cost*10)

            print("Route taken:")
            for cell in path:
                if maze[cell[0]][cell[1]] not in ['S', 'G']:
                    maze[cell[0]][cell[1]] = 'P'
            for row in maze:
                print(' '.join(row))
            return
        
        visited.add((x, y))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < row and 0 <= new_y < cols and maze[new_x][new_y] != 'W' and (new_x, new_y) not in visited:
                new_cost = cost + 1
                new_heuristic = heuristic(new_x, new_y, goal_x, goal_y)
                new_priority = new_cost + new_heuristic
                heapq.heappush(priority_queue, (new_priority, new_cost, new_x, new_y))
                previous_visitors[(new_x, new_y)] = (x, y)

    print("A* Search: No solution found")

valid_move_astar(m, n, maze, startingX, startingY, goal_x, goal_y)
