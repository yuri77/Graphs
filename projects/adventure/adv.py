from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque

"""
ast.literal_eval: Safely evaluate an expression node or a string containing 
a Python literal or container display. The string or node provided may only
consist of the following Python literal structures: strings, bytes, numbers,
tuples, lists, dicts, sets, booleans, None, bytes and sets.
"""

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = set()
# Deque(Double-Ended Queue) support thread-safe, memory efficient appends and pops
# from either side of the deque with approximately the same O(1) performance in either direction.
d = deque()
backward = {'s': 'n', 'n': 's', 'w': 'e', 'e': 'w'}
# comparing visited to len of rooms to ensure a complete traversal
while len(visited) < len(world.rooms):
    # all direction that room can go
    exits = player.current_room.get_exits()
    """
    print(exits)
    output for room 0 : ['n', 's', 'w', 'e']
    """
    path = []
    for i in exits:
        # if exit exists and we haven't visited
        if i is not None and player.current_room.get_room_in_direction(i) not in visited:
            """
            print(player.current_room.get_room_in_direction(i))
            output: Room 4  (13,17)  Exits: [s]
            """
            path.append(i)
            """
            print(path)
            ['n','s','w','e']
            """
    # add the current room to the visited
    visited.add(player.current_room)
    """
    print(player.current_room)
    output : Room 0  (13,16)  Exits: [n, s, w, e]
    """
    if len(path) > 0:
        # randomly choose  direction to go
        direction = path[random.randint(0, len(path) - 1)]
        d.append(direction)
        player.travel(direction)
        traversal_path.append(direction)
    else:
        prev_room = d.pop()  # Pop the top of the deque (Queue like)
        # the direction now change to backward[prev_room]
        player.travel(backward[prev_room])
        # the meantime the current room changed to next_room with the new direction
        traversal_path.append(backward[prev_room])


print(traversal_path)
# print(len(traversal_path))


# TRAVERSAL TEST
visited_rooms = set()

player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
