import random
import heapq

# Task 1

# creating the maze using list
maze = [
    [0, 6, 12, 18, 24, 30],
    [1, 7, 13, 19, 25, 31],
    [2, 8, 14, 20, 26, 32],
    [3, 9, 15, 21, 27, 33],
    [4, 10, 16, 22, 28, 34],
    [5, 11, 17, 23, 29, 35]
]

# defining start,goal and barrier node
start_node = random.randint(0, 11)
goal_node = random.randint(24, 35)

# getting a list of nodes other than the start and goal node
remaining_nodes = [node for row in maze for node in row if node != start_node and node != goal_node]
# out of the remaining nodes getting 4 random nodes
barrier_nodes = random.sample(remaining_nodes, 4)
print("Barrier Nodes - " + str(barrier_nodes))
print()

# visual representation of the maze with start, goal and barriers
def display_maze():
    for row in maze:
        for node in row:
            if node == start_node:
                print("S", end=" ")
            elif node == goal_node:
                print("G", end=" ")
            elif node in barrier_nodes:
                print("#", end=" ")
            else:
                print(node, end=" ")
        print()


# call the display_maze function to see the maze
display_maze()

# Task 2

# initializing direction vectors
Horizontal = [-1, 0, 1, 0, -1, 1, 1, -1]
Vertical = [0, -1, 0, 1, -1, -1, 1, 1]

# check whether the move is going to be valid
def is_valid_move(x, y, barrier_nodes, visited):
    # checks whether it's inside the boundaries of the maze and whether there is a barrier or not
    if (x < 0 or y < 0 or x >= 6 or y >= 6 or (x * 6 + y) in barrier_nodes):
        return False
    # checks whether the node is already visited
    if (x * 6 + y in visited):
        return False

    return True

# depth first search algorithm
def dfs(start_node, goal_node, barrier_nodes):
    stack = [(start_node, [start_node])]  # a stack that has a tuple of current node and path
    visited = set()  # a set that tracks visited nodes

    while stack:  # iterates until goal is reached
        curr_node, path = stack.pop()  # remove and take the top element of the stack
        x, y = divmod(curr_node, 6)  # converting the node into coordinates

        if curr_node == goal_node:  # checks whether goal is reached
            return path, len(visited)
        # iterates over the eight possible directions from the current node and takes their coordinates and are
        # sorted according to the increasing order
        neighbours = sorted([(x + Horizontal[i], y + Vertical[i]) for i in range(8)],
                            key=lambda pos: (pos[1], pos[0]))  # sorts the list of coordinates based on the second
        # element (y-coordinate) first and then the first element (x-coordinate)

        # if goal node is a neighbor it will get chosen first
        goal_neighbor = (goal_node // 6, goal_node % 6)  # extract row and column coordinates for the goal node
        # checks if goal node is in neighbors and is a valid move
        if goal_neighbor in neighbours and is_valid_move(goal_neighbor[0], goal_neighbor[1], barrier_nodes, visited):
            visited.add(curr_node)  # mark the current node as visited
            stack.append((goal_node, path + [goal_node]))  # goal node added to the stack
            continue

        for neighbour_X, neighbour_Y in neighbours:
            if not is_valid_move(neighbour_X, neighbour_Y, barrier_nodes, visited):  # check whether the move is valid
                continue  # if invalid it will go to the next iteration

            visited.add(curr_node)
            neighbour_node = neighbour_X * 6 + neighbour_Y  # convert the coordinate into node index
            stack.append((neighbour_node, path + [neighbour_node]))  # neighbor node added to the stack
    # if the stack becomes empty and the goal is not reached
    return [], len(visited)


path, nodes_visited = dfs(start_node, goal_node, barrier_nodes)
print("-----------------Depth First Search-----------------")
print("Visited Nodes:", path)
print("Time to Find Goal (in minutes):", nodes_visited)
print("Final Path:", path)
print("")


# Task 3
def manhattan_dis(maze, goal_node):  # maze to iterate through each node and goal node to get its coordinates
    heu_costs = {}  # dictionary to show heuristic costs for each node
    goal_x, goal_y = divmod(goal_node, 6)  # getting x and y coordinates of goal
    for row in maze:  # iterating through maze
        for node in row:  # each node in each row
            curr_x, curr_y = divmod(node, 6)  # coordinates of the current node
            heu_cost = abs(curr_x - goal_x) + abs(curr_y - goal_y)  # equation for manhattan distance
            heu_costs[node] = heu_cost  # stores the heuristic cost in the dictionary

    return heu_costs


final_heuristic_costs = manhattan_dis(maze, goal_node)

# for node, cost in final_heuristic_costs.items():  # printing each h cost for each node
#     print(f"Heuristic cost for node {node}: {cost}")


# Task 4

def a_star_search(start_node, goal_node, barrier_nodes):
    priority_queue = [(0, start_node, [start_node])]  # initializing a priority queue with a tuple having total cost,
    # current node, and the path
    visited = set()  # to keep track of visited nodes

    while priority_queue:  # runs as long as it's not empty
        _, curr_node, path = heapq.heappop(priority_queue)  # pops the node with the lowest heuristic cost from the
        # queue. the heu cost is ignored and others are taken

        if curr_node == goal_node:  # checks whether its goal node
            return path, len(visited)

        x, y = divmod(curr_node, 6)  # gets the coordinates of the current node
        neighbours = sorted([(x + Horizontal[i], y + Vertical[i]) for i in range(8)],
                            key=lambda pos: (pos[1], pos[0]))  # sorts the list of coordinates based on the second
        # element (y-coordinate) first and then the first element (x-coordinate)

        for neighbour_X, neighbour_Y in neighbours:
            if not is_valid_move(neighbour_X, neighbour_Y, barrier_nodes, visited): # check whether the move is valid
                continue  # if invalid it will go to the next iteration

            visited.add(curr_node)
            neighbour_node = neighbour_X * 6 + neighbour_Y  # convert the coordinate into node index
            cost_neighbour = len(path) + 1 + final_heuristic_costs[neighbour_node]  # getting the total cost to reach
            # the neighbour node considering the length of path,
            # cost to move to neighbour and manhandle distance cost
            heapq.heappush(priority_queue, (cost_neighbour, neighbour_node, path + [neighbour_node]))
            # pushes a tuple into the priority queue containing the total cost, the neighbor node, and the updated path

    return [], len(visited)


path, nodes_visited = a_star_search(start_node, goal_node, barrier_nodes)
print("-----------------A Star Search-----------------")
print("Visited Nodes:", path)
print("Time to Find Goal (in minutes):", nodes_visited)
print("Final Path:", path)
print("")
