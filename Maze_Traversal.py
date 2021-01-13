import random
from copy import deepcopy
from math import sqrt


def display_maze_path(maze, path, search_method):
    for position in path:
        maze[position[0]][position[1]] = 'o'
    transposed_maze = deepcopy(maze)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            transposed_maze[i][j] = maze[j][len(maze)-1-i]
    print(search_method + " from " + str(path[0]) + " to " + str(path[-1]))
    for rows in transposed_maze:
        print(rows)


def breadth_first_search(maze, start_x, start_y, end_x, end_y):
    start_pos = [start_x, start_y]
    end_pos = [end_x, end_y]
    open_list = [start_pos]
    closed_list = []
    parent_dict = dict()
    # if the first position in the open_list is the end_position
    while len(open_list) > 0 and open_list[0] != end_pos:
        # first in first out for BFS, so the current position is always the first node in the open_list
        curr_pos = open_list[0]
        # four possible directions as next nodes
        directions = generate_directions(curr_pos)
        for direction in directions:
            # checks if the node is already in the list, if the node is within the maze boundary, and if the place
            # the node is a block or not
            if direction not in open_list and direction not in closed_list and 0 <= direction[0] < 25 and \
                    0 <= direction[1] < 25 and maze[direction[0]][direction[1]] != 'x':
                open_list.append(direction)
                parent_dict[tuple(direction)] = curr_pos
        closed_list.append(curr_pos)
        open_list = open_list[1:]
    if len(open_list) == 0:
        return "Solution not found"
    path = backtrace(parent_dict, start_pos, end_pos)
    # shows a graphical representation of the path took by the searching algorithm
    display_maze_path(deepcopy(maze), path, "BFS")
    return path, len(path), len(closed_list)


def depth_first_search(maze, start_x, start_y, end_x, end_y):
    start_pos = [start_x, start_y]
    end_pos = [end_x, end_y]
    open_list = [start_pos]
    closed_list = []
    parent_dict = dict()
    # if the last position in the open_list is the end_position
    while len(open_list) > 0 and open_list[-1] != end_pos:
        # last in first out for DFS, so the current position is always the last node in the open_list
        curr_pos = open_list[-1]
        # four possible directions as next nodes
        directions = generate_directions(curr_pos)
        random.shuffle(directions)
        dead_end = True
        for direction in directions:
            # checks if the node is already in the list, if the node is within the maze boundary, and if the place
            # the node is a block or not
            if direction not in open_list and direction not in closed_list and 0 <= direction[0] < 25 and \
                    0 <= direction[1] < 25 and maze[direction[0]][direction[1]] != 'x':
                dead_end = False
                open_list.append(direction)
                parent_dict[tuple(direction)] = curr_pos
        if curr_pos not in closed_list:
            closed_list.append(curr_pos)
        # checks if a dead end has been reached, and if so remove it from the stack
        if dead_end:
            open_list = open_list[:-1]
    if len(open_list) == 0:
        return "Solution not found"
    path = backtrace(parent_dict, start_pos, end_pos)
    # shows a graphical representation of the path took by the searching algorithm
    display_maze_path(deepcopy(maze), path, "DFS")
    return path, len(path), len(closed_list)


def heuristic(curr_pos, end_pos):
    # this heuristic calculates the euclidean distance from the current position to the end position
    return sqrt(pow(curr_pos[0]-end_pos[0], 2) + pow(curr_pos[1]-end_pos[1], 2))


def append_heuristics(arr, g, h):
    arr.append(g)
    arr.append(h)
    arr.append(g + h)


def generate_directions(curr_pos):
    up = [curr_pos[0], curr_pos[1] + 1]
    down = [curr_pos[0], curr_pos[1] - 1]
    left = [curr_pos[0] - 1, curr_pos[1]]
    right = [curr_pos[0] + 1, curr_pos[1]]
    return [up, down, left, right]


def a_star(maze, start_x, start_y, end_x, end_y):
    start_pos = [start_x, start_y]
    end_pos = [end_x, end_y]
    g = 0
    h = heuristic(start_pos, end_pos)
    append_heuristics(start_pos, g, h)
    open_list = [start_pos]
    closed_list = []
    parent_dict = dict()
    # if the first position in the open_list is the end_position,
    while len(open_list) > 0 and open_list[0][:-3] != end_pos:
        # first in first out for BFS, so the current position is always the first node in the open_list
        curr_pos = open_list[0]
        curr_g = curr_pos[2] + 1
        # four possible directions as next nodes
        directions = generate_directions(curr_pos)
        for direction in directions:
            # checks if the node is already in the list, if the node is within the maze boundary, and if the place
            # the node is a block or not
            curr_heuristic = heuristic(direction, end_pos)
            append_heuristics(direction, curr_g, curr_heuristic)
            for positions in open_list:
                # checking if there is a better heuristic for a previous location, and if so, update the heuristic
                if positions[0] == direction[0] and positions[1] == direction[1] and positions[4] > direction[4]:
                    positions[2] = direction[2]
                    positions[3] = direction[3]
                    # update the parent of the direction to be the current position
                    parent_dict[tuple(direction[:-3])] = curr_pos[:-3]
            if direction not in open_list and direction[:-3] not in closed_list and 0 <= direction[0] < 25 and \
                    0 <= direction[1] < 25 and maze[direction[0]][direction[1]] != 'x':
                open_list.append(direction)
                parent_dict[tuple(direction[:-3])] = curr_pos[:-3]
        closed_list.append(curr_pos[:-3])
        open_list = open_list[1:]
        # sort the list to order the best heuristic first
        open_list = sorted(open_list, key=lambda x: x[4])
    if len(open_list) == 0:
        return "Solution not found"
    path = backtrace(parent_dict, start_pos[:-3], end_pos)
    # shows a graphical representation of the path took by the searching algorithm
    display_maze_path(deepcopy(maze), path, "A*")
    return path, len(path), len(closed_list)


def backtrace(parent_dict, start_pos, end_pos):
    path = [end_pos]
    curr_pos = end_pos
    while curr_pos != start_pos:
        path.append(parent_dict[tuple(curr_pos)])
        curr_pos = parent_dict[tuple(curr_pos)]
    return list(reversed(path))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_maze = [
        [' ', ' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', 'x', 'x', ' '],
        [' ', ' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', 'x', 'x', ' '],
        [' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', 'x', 'x', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', 'x', 'x', 'x', 'x', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', 'x', 'x', 'x', 'x', 'x'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', 'x', 'x', ' ', 'x', 'x'],
        [' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', 'x', ' '],
        [' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', 'x', 'x', 'x', 'x', 'x', 'x', 'x', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', 'x', ' '],
        [' ', ' ', 'x', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', 'x', 'x', 'x', ' ', ' ', ' ', ' '],
        [' ', ' ', 'x', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', 'x', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x', 'x', 'x', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', 'x', ' ', 'x', 'x', 'x', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', 'x', ' ', 'x', 'x', 'x', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x', 'x', 'x', ' ', 'x'],
        [' ', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x', 'x', 'x', ' ', 'x'],
        [' ', 'x', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x', 'x', 'x', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x', 'x', 'x', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', 'x', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    ]
    ans_arr = ["Path Found: ", "Cost: ", "Number of Nodes Explored: "]
    search_arr = ["BFS: ", "DFS: ", "A*: "]
    total_arr = [[], [], []]
    start_coordinates = [[2, 11], [2, 11], [0, 0]]
    end_coordinates = [[23, 19], [2, 21], [24, 24]]
    for i in range(len(total_arr)):
        total_arr[i].append(breadth_first_search(main_maze, start_coordinates[i][0], start_coordinates[i][1], end_coordinates[i][0], end_coordinates[i][1]))
        total_arr[i].append(depth_first_search(main_maze, start_coordinates[i][0], start_coordinates[i][1], end_coordinates[i][0], end_coordinates[i][1]))
        total_arr[i].append(a_star(main_maze, start_coordinates[i][0], start_coordinates[i][1], end_coordinates[i][0], end_coordinates[i][1]))
    for i in range(len(total_arr)):
        print("From " + str(start_coordinates[i]) + " to " + str(end_coordinates[i]))
        for j in range(len(total_arr[i])):
            print(search_arr[j])
            for k in range(len(total_arr[j])):
                print(ans_arr[k] + str(total_arr[i][j][k]))
