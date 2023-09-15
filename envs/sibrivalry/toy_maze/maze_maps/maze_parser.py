from queue import Queue
# Parse function for labyrinths from https://movingai.com/benchmarks/maze/index.html
# Grid size - size of one cell
# Structure of file: One line of wall (either present: '@', or absent: '.'), 2^k (In default case, k=5) lines of room interior.
def get_maze(maze_type="10x10"):
    
    if maze_type == "10x10":
        return MAZE_10x10
    
    elif maze_type == "16x16":
        maze_type = "envs/sibrivalry/toy_maze/maze_maps/maze_layouts/maze512-32-9.map"
    file_name = maze_type.split("/")[-1]
    info = file_name.split("-")
    chars_in_line = int(info[0][4:])
    chars_in_room = int(info[1])

    ascii_maze_file = open(maze_type, "r")
    ascii_maze = ascii_maze_file.read()
    ascii_maze_file.close()
    maze_lines = ascii_maze.split("\n")

    starting_char = 1
    room_size = chars_in_room
    wall_size = 1
    graph = {}
    for i in range(chars_in_line//chars_in_room+1):
        for j in range(chars_in_line//chars_in_room+1):
            graph[(i, j)] = []
    
    maze_size = -1.
    for i in range(starting_char, chars_in_line, (room_size+wall_size)):
        node_i = (i-starting_char)//(room_size+wall_size)
        for j in range(starting_char, chars_in_line, (room_size+wall_size)):
            node_j = (j-starting_char)//(room_size+wall_size)
            node = (node_j, node_i)
            if i+room_size<chars_in_line and maze_lines[i+room_size][j] == '.':
                graph[node].append((node_j, node_i+1))
                graph[(node_j, node_i+1)].append(node)
            if j+room_size<chars_in_line and maze_lines[i][j+room_size] == '.':
                graph[node].append((node_j+1, node_i))
                graph[(node_j+1, node_i)].append(node)
            maze_size = max(maze_size, node_i + 1, node_j + 1)
    maze_size = float(maze_size)
    
    sibrivalry_maze_format = []
    visited = set()
    queue = Queue()
    queue.put({"node": (0, 0), "ancestor": None})
    while not queue.empty():
        current_node = queue.get()
        node, ancestor = current_node["node"], current_node["ancestor"]
        for successor in graph[node]:
            if successor not in visited:
                queue.put({"node": successor, "ancestor": node})
        
        if ancestor is not None:
            sibrivalry_maze_format.append(convert_to_sibrivalry_node_format(ancestor, node))
        visited.add(node)

    action_range = 0.95
    goal_squares = ["0,15", "15,15", "15,0", "5,12", "12,5", "8,8"]
    return (sibrivalry_maze_format, maze_size, action_range, goal_squares)


def convert_to_sibrivalry_node_format(ancestor, node):
    
    if ancestor == (0, 0):
        ancestor_name = "origin"
    else:
        ancestor_name = "{},{}".format(ancestor[0], ancestor[1])
    
    node_name = "{},{}".format(node[0], node[1])
    
    if node[0] - ancestor[0] == 1:
        direction = "right"
    elif node[0] - ancestor[0] == -1:
        direction = "left"
    elif node[1] - ancestor[1] == 1:
        direction = "up"
    elif node[1] - ancestor[1] == -1:
        direction = "down"
    
    return {"anchor": ancestor_name, "direction": direction, "name": node_name}

MAZE_10x10 = ([
     {'anchor': 'origin', 'direction': 'right', 'name': '1,0'},
     {'anchor': 'origin', 'direction': 'up', 'name': '0,1'},
     {'anchor': '1,0', 'direction': 'right', 'name': '2,0'},
     {'anchor': '0,1', 'direction': 'up', 'name': '0,2'},
     {'anchor': '0,2', 'direction': 'right', 'name': '1,2'},
     {'anchor': '2,0', 'direction': 'up', 'name': '2,1'},
     {'anchor': '1,2', 'direction': 'right', 'name': '2,2'},
     {'anchor': '0,2', 'direction': 'up', 'name': '0,3'},
     {'anchor': '2,1', 'direction': 'right', 'name': '3,1'},
     {'anchor': '1,2', 'direction': 'down', 'name': '1,1'},
     {'anchor': '3,1', 'direction': 'down', 'name': '3,0'},
     {'anchor': '1,2', 'direction': 'up', 'name': '1,3'},
     {'anchor': '3,1', 'direction': 'right', 'name': '4,1'},
     {'anchor': '1,3', 'direction': 'up', 'name': '1,4'},
     {'anchor': '4,1', 'direction': 'right', 'name': '5,1'},
     {'anchor': '4,1', 'direction': 'up', 'name': '4,2'},
     {'anchor': '5,1', 'direction': 'down', 'name': '5,0'},
     {'anchor': '3,0', 'direction': 'right', 'name': '4,0'},
     {'anchor': '1,4', 'direction': 'right', 'name': '2,4'},
     {'anchor': '4,2', 'direction': 'right', 'name': '5,2'},
     {'anchor': '2,4', 'direction': 'right', 'name': '3,4'},
     {'anchor': '3,4', 'direction': 'up', 'name': '3,5'},
     {'anchor': '1,4', 'direction': 'left', 'name': '0,4'},
     {'anchor': '1,4', 'direction': 'up', 'name': '1,5'},
     {'anchor': '2,2', 'direction': 'up', 'name': '2,3'},
     {'anchor': '3,1', 'direction': 'up', 'name': '3,2'},
     {'anchor': '5,0', 'direction': 'right', 'name': '6,0'},
     {'anchor': '3,2', 'direction': 'up', 'name': '3,3'},
     {'anchor': '4,2', 'direction': 'up', 'name': '4,3'},
     {'anchor': '6,0', 'direction': 'up', 'name': '6,1'},
     {'anchor': '6,0', 'direction': 'right', 'name': '7,0'},
     {'anchor': '6,1', 'direction': 'right', 'name': '7,1'},
     {'anchor': '3,4', 'direction': 'right', 'name': '4,4'},
     {'anchor': '1,5', 'direction': 'right', 'name': '2,5'},
     {'anchor': '7,1', 'direction': 'up', 'name': '7,2'},
     {'anchor': '1,5', 'direction': 'up', 'name': '1,6'},
     {'anchor': '4,4', 'direction': 'right', 'name': '5,4'},
     {'anchor': '5,4', 'direction': 'down', 'name': '5,3'},
     {'anchor': '0,4', 'direction': 'up', 'name': '0,5'},
     {'anchor': '7,2', 'direction': 'left', 'name': '6,2'},
     {'anchor': '1,6', 'direction': 'left', 'name': '0,6'},
     {'anchor': '7,0', 'direction': 'right', 'name': '8,0'},
     {'anchor': '7,2', 'direction': 'right', 'name': '8,2'},
     {'anchor': '2,5', 'direction': 'up', 'name': '2,6'},
     {'anchor': '8,0', 'direction': 'up', 'name': '8,1'},
     {'anchor': '3,5', 'direction': 'up', 'name': '3,6'},
     {'anchor': '6,2', 'direction': 'up', 'name': '6,3'},
     {'anchor': '6,3', 'direction': 'right', 'name': '7,3'},
     {'anchor': '3,5', 'direction': 'right', 'name': '4,5'},
     {'anchor': '7,3', 'direction': 'up', 'name': '7,4'},
     {'anchor': '6,3', 'direction': 'up', 'name': '6,4'},
     {'anchor': '6,4', 'direction': 'up', 'name': '6,5'},
     {'anchor': '8,1', 'direction': 'right', 'name': '9,1'},
     {'anchor': '8,2', 'direction': 'right', 'name': '9,2'},
     {'anchor': '2,6', 'direction': 'up', 'name': '2,7'},
     {'anchor': '8,2', 'direction': 'up', 'name': '8,3'},
     {'anchor': '6,5', 'direction': 'left', 'name': '5,5'},
     {'anchor': '5,5', 'direction': 'up', 'name': '5,6'},
     {'anchor': '7,4', 'direction': 'right', 'name': '8,4'},
     {'anchor': '8,4', 'direction': 'right', 'name': '9,4'},
     {'anchor': '0,6', 'direction': 'up', 'name': '0,7'},
     {'anchor': '2,7', 'direction': 'up', 'name': '2,8'},
     {'anchor': '7,4', 'direction': 'up', 'name': '7,5'},
     {'anchor': '9,4', 'direction': 'down', 'name': '9,3'},
     {'anchor': '9,4', 'direction': 'up', 'name': '9,5'},
     {'anchor': '2,7', 'direction': 'left', 'name': '1,7'},
     {'anchor': '4,5', 'direction': 'up', 'name': '4,6'},
     {'anchor': '9,1', 'direction': 'down', 'name': '9,0'},
     {'anchor': '6,5', 'direction': 'up', 'name': '6,6'},
     {'anchor': '3,6', 'direction': 'up', 'name': '3,7'},
     {'anchor': '1,7', 'direction': 'up', 'name': '1,8'},
     {'anchor': '3,7', 'direction': 'right', 'name': '4,7'},
     {'anchor': '2,8', 'direction': 'up', 'name': '2,9'},
     {'anchor': '2,9', 'direction': 'left', 'name': '1,9'},
     {'anchor': '7,5', 'direction': 'up', 'name': '7,6'},
     {'anchor': '1,8', 'direction': 'left', 'name': '0,8'},
     {'anchor': '6,6', 'direction': 'up', 'name': '6,7'},
     {'anchor': '0,8', 'direction': 'up', 'name': '0,9'},
     {'anchor': '7,5', 'direction': 'right', 'name': '8,5'},
     {'anchor': '6,7', 'direction': 'left', 'name': '5,7'},
     {'anchor': '2,9', 'direction': 'right', 'name': '3,9'},
     {'anchor': '3,9', 'direction': 'right', 'name': '4,9'},
     {'anchor': '7,6', 'direction': 'right', 'name': '8,6'},
     {'anchor': '3,7', 'direction': 'up', 'name': '3,8'},
     {'anchor': '9,5', 'direction': 'up', 'name': '9,6'},
     {'anchor': '7,6', 'direction': 'up', 'name': '7,7'},
     {'anchor': '5,7', 'direction': 'up', 'name': '5,8'},
     {'anchor': '3,8', 'direction': 'right', 'name': '4,8'},
     {'anchor': '8,6', 'direction': 'up', 'name': '8,7'},
     {'anchor': '5,8', 'direction': 'right', 'name': '6,8'},
     {'anchor': '7,7', 'direction': 'up', 'name': '7,8'},
     {'anchor': '4,9', 'direction': 'right', 'name': '5,9'},
     {'anchor': '8,7', 'direction': 'right', 'name': '9,7'},
     {'anchor': '7,8', 'direction': 'right', 'name': '8,8'},
     {'anchor': '8,8', 'direction': 'up', 'name': '8,9'},
     {'anchor': '5,9', 'direction': 'right', 'name': '6,9'},
     {'anchor': '6,9', 'direction': 'right', 'name': '7,9'},
     {'anchor': '8,9', 'direction': 'right', 'name': '9,9'},
     {'anchor': '9,9', 'direction': 'down', 'name': '9,8'}
], 10., 0.95, ['9,9', '9,4', '9,0', '6,9', '6,4', '6,0', '3,9', '3,4', '3,0', '0,9', '0,4'])