from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

############################
### Start of Sprint Code ###
############################

def graph_add(room):
    "Add all exits in current room and assign ? as values"
    graph[room.id] = {k:"?" for k in room.get_exits()}
    return

def update_graph(direction, room):
    "Update graph with connected room"
    if direction == "n":
        graph[room.id][direction] = room.n_to.id
    elif direction == "e":
        graph[room.id][direction] = room.e_to.id
    elif direction == "w":
        graph[room.id][direction] = room.w_to.id
    elif direction == "s":
        graph[room.id][direction] = room.s_to.id
    else:
        print("That is not a valid direction (update_graph)")
    return

def find_room(direction, room):
    "Return the room ID of the desired direction"
    if direction == "n":
        return room.n_to.id 
    if direction == "e":
        return room.e_to.id
    if direction == "w":
        return room.w_to.id 
    if direction == "s":
        return room.s_to.id 
    else:
        print("Not a valid direction")
    return

def find_opposite(direction):
    "Return the opposite direction"
    if direction == "n":
        return "s"
    elif direction == "e":
        return "w"
    elif direction == "s":
        return "n"
    elif direction == "w":
        return "e"
    else:
        print("That is not a valid direction (find_opposite)")   

def room_check(room):
    "Check if the current room has any unexplored exits"
    check = [True for k,v in graph[player.current_room.id].items() if v == "?"]
    return True if len(check) > 0 else False
    
def dft_recursive(direction):
    "Recursively search in one direction until a room no longer has an exit with the inputted direction"
    # Base cases
    if len(visited) == len(room_graph):
        return
    if direction not in player.current_room.get_exits():
        return
      
    # If room is not in graph then add room and intialize all possible exits with ?
    if player.current_room.id not in graph:
        graph_add(player.current_room)
    
    # Update graph room exit with value if values are in visited
    update_graph(direction, player.current_room)

    # Add direction to traversal path and call itself
    traversal_path.append(direction)
    player.travel(direction)
    visited.add(player.current_room.id)

    dft_recursive(direction)

# Instantiate graph to hold rooms and exits
graph = {}

# Add seed room to graph
graph_add(player.current_room)

# Track visited rooms
visited = set()
visited.add(player.current_room.id)
counter_start = 0
# Iterate over graph while rooms visited is not equal to length room graph
while len(visited) != len(room_graph):

    # If room is not in graph then add room and intialize all possible exits with ?
    if player.current_room.id not in graph:
        graph_add(player.current_room)

    # Iterate over key in current room saved in graph
    for x in graph[player.current_room.id]:

        # Start by going east
        if counter_start == 0:
            x = "e"
            counter_start+=1

        # Logging
        print("Current Room:",player.current_room.id,"Current Direction:", x)
        print("Current Room Keys:", graph[player.current_room.id])
        print("Total Moves", len(traversal_path))
        print("Visited:", len(visited), "Total Rooms:", len(room_graph), "\n")

        # If the current x value does not exist in the keys then continue to next value
        if x not in graph[player.current_room.id].keys():
            continue

        # If direction value is ? then go that direction if not in visited
        elif (graph[player.current_room.id][x] == "?") and (find_room(x, player.current_room) not in visited):
            dft_recursive(x)
            print("Enter dft")
            break
        
        # If current direction is to a  ? and other ? exist in room then continue to other ?
        elif (graph[player.current_room.id][x] == "?") and ("?" in [v for k,v in graph[player.current_room.id].items() if k != x]):
            print("Enter continue")
            continue
        
        # If ? exit is present and next room is visited move one space and restart loop
        elif graph[player.current_room.id][x] == "?" and find_room(x, player.current_room) in visited:
            traversal_path.append(x)
            update_graph(x, player.current_room)
            player.travel(x)
            print("Enter one step")
            break

        # Take a step backwards and see if there are any un explored exits
        else:
            print("Enter else", "Room Check:", room_check(player.current_room.id))
            # Keep track of index location of next backwards step
            count = -1

            # Make copy of traversal path to use
            temp_traversal = traversal_path.copy()

            # Return direction of unvisted rooms in current room
            check = [k for k,v in graph[player.current_room.id].items() if v == "?" and find_room(k, player.current_room) in visited]

            # Keep walking backwards until a unexplored exit is found
            for _ in range(len(temp_traversal)):
                if room_check(player.current_room.id) == False:

                    # Find opposite direction to go backwards
                    opp = find_opposite(temp_traversal[count])

                    # Add backwards step to traversal path
                    traversal_path.append(opp)

                    print("Walking Backwards")
                    # Travel backwards
                    player.travel(opp)

                    # Add room to visited
                    visited.add(player.current_room.id)

                    # Update count and room check
                    count -= 1

                # If rooms all rooms are visited and only known exit exists go in the opposite directiom of the known exit
                elif room_check(player.current_room.id) == True and len(check) > 1:
                    print("Enter elif in walk backwards, Current direction:", x)
                    opposite = find_opposite(x)
                    traversal_path.append(opposite)
                    update_graph(opposite, player.current_room)
                    player.travel(opposite)
                    print("Walk in opposite direction")
                    break
                else:
                    break

print(traversal_path)
##########################
### End of Sprint Code ###
##########################

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
