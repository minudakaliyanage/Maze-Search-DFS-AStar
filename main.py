import random
from queue import PriorityQueue

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
print()


# visual representation of the maze with start, goal and barriers
def display_maze():
    for row in maze:
        for node in row:
            if node == start_node:
                print("\033[92m{: <4}\033[0m".format("S"), end=" ")  # Green color for start node
            elif node == goal_node:
                print("\033[91m{: <4}\033[0m".format("G"), end=" ")  # Red color for goal node
            elif node in barrier_nodes:
                print("\033[94m{: <4}\033[0m".format("#"), end=" ")  # Blue color for barrier nodes
            else:
                print("{: <4}".format(node), end=" ")  # Default formatting
        print()


# call the display_maze function to see the maze
display_maze()
print()

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
    explored = []
    while stack:  # iterates until goal is reached
        curr_node, path = stack.pop()  # remove and take the top element of the stack
        x, y = divmod(curr_node, 6)  # converting the node into coordinates

        if curr_node == goal_node:  # checks whether goal is reached
            return path, len(explored)
        # iterates over the eight possible directions from the current node and takes their coordinates and are
        # sorted according to the increasing order
        neighbours = sorted([(x + Horizontal[i], y + Vertical[i]) for i in range(8)],
                            key=lambda pos: (pos[1], pos[0]))  # sorts the list of coordinates based on the second
        # element (y-coordinate) first and then the first element (x-coordinate)

        for neighbour_X, neighbour_Y in neighbours:
            if not is_valid_move(neighbour_X, neighbour_Y, barrier_nodes, visited):  # check whether the move is valid
                continue  # if invalid it will go to the next iteration
            visited.add(curr_node)
            neighbour_node = neighbour_X * 6 + neighbour_Y  # convert the coordinate into node index
            explored.append(neighbour_node)
            stack.append((neighbour_node, path + [neighbour_node]))  # neighbor node added to the stack
    # if the stack becomes empty and the goal is not reached
    return [], len(explored)


path, nodes_explored = dfs(start_node, goal_node, barrier_nodes)
print("-----------------Depth First Search-----------------")
print("Visited Nodes:", path)
print("Time to Find Goal (in minutes):", nodes_explored)
print("Final Path:", path)
print("")


# Task 3
def heuristic_cost(node, goal_node):
    goal_x, goal_y = divmod(goal_node, 6)  # getting x and y coordinates of the goal node
    curr_x, curr_y = divmod(node, 6)  # coordinates of the current node
    heu_cost = abs(curr_x - goal_x) + abs(curr_y - goal_y)  # equation for Manhattan distance
    return heu_cost


# Task 4
def a_star_search(start_node, goal_node, barrier_nodes):
    # Initialize a dictionary to store the cost to reach each node, initially set to infinity
    cost_so_far = {node: float('inf') for node in barrier_nodes}
    cost_so_far[start_node] = 0
    # Initialize a dictionary to store the total cost for each node, initially set to infinity
    total_cost = {node: float('inf') for node in barrier_nodes}
    total_cost[start_node] = heuristic_cost(start_node, goal_node)
    # Initialize a priority queue to prioritize nodes based on their total cost
    priority_queue = PriorityQueue()
    priority_queue.put((heuristic_cost(start_node, goal_node), heuristic_cost(start_node, goal_node), start_node))
    # Initialize dictionaries to store the path and set to store visited nodes
    path = {}
    visited = set()

    while not priority_queue.empty():
        # Get the node with the lowest total cost from the priority queue
        curr_node = priority_queue.get()[2]
        # Check if the goal node is reached
        if curr_node == goal_node:
            break

        x, y = divmod(curr_node, 6)  # gets the coordinates of the current node
        neighbours = [(x + Horizontal[i], y + Vertical[i]) for i in range(8)]  # Generate neighbors of the current node

        for neighbour_X, neighbour_Y in neighbours:
            if not is_valid_move(neighbour_X, neighbour_Y, barrier_nodes, visited):  # check whether the move is valid
                continue  # if invalid it will go to the next iteration
            # convert to node index from x and y coordinates
            neighbour_node = neighbour_X * 6 + neighbour_Y
            # Initialize cost for the neighbor if not present in total_cost
            if neighbour_node not in total_cost:
                total_cost[neighbour_node] = float('inf')
            # Calculate indefinite cost to reach the neighbor
            temp_cost_so_far = cost_so_far[curr_node] + 1
            temp_total_cost = temp_cost_so_far + heuristic_cost(neighbour_node, goal_node)
            # Mark the neighbor as visited
            visited.add(neighbour_node)
            # Check if the newly calculated total cost to reach the neighbor is less than the previously recorded
            # total cost
            if temp_total_cost < total_cost[neighbour_node]:
                # Update the cost to reach the neighbor so far
                cost_so_far[neighbour_node] = temp_cost_so_far
                # Update the total cost to reach the neighbor
                total_cost[neighbour_node] = temp_total_cost
                # Put the neighbor in the priority queue with its updated total cost and heuristic cost
                priority_queue.put((temp_total_cost, heuristic_cost(neighbour_node, goal_node), neighbour_node))
                # Record the current node as the predecessor for the neighbor in the path dictionary
                path[neighbour_node] = curr_node

    forward_path = []
    curr_node = goal_node  # Set the current node to be the goal node
    # Continue looping until the current node reaches the start node
    while curr_node != start_node:
        forward_path.append(curr_node)  # Add the current node to the forward path
        curr_node = path[curr_node]  # Update the current node to its predecessor in the path dictionary

    forward_path.append(start_node)  # Add the start node to the forward path
    forward_path.reverse()  # Reverse the forward path to obtain the correct order from start to goal

    return list(visited), forward_path


nodes_visited, final_path = a_star_search(start_node, goal_node, barrier_nodes)
print("-----------------A Star Search-----------------")
print("Visited Nodes:", nodes_visited)
print("Time to Find Goal (in minutes):", len(nodes_visited))
print("Final Path:", final_path)
print("")
