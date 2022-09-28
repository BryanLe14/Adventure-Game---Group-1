from getkey import getkey, keys
from emoji import emojize, is_emoji

def check_collision(direction, world_list, location, items):
    """Checks player movement (WASD) for collisions"""
    row = location[0]
    col = location[1]

    # print(world_list[row-1][col])
    # input()
    
    if direction.upper() == "W" or direction == keys.UP:
        if world_list[row-1][col] != "#":
            location = [row-1, col]
            world_list[row-1][col] = "P"
            world_list[row][col] = "/"
        else:
            location = [row, col]            
    elif direction.upper() == "S" or direction == keys.DOWN:
        if world_list[row+1][col] != "#":
            location = [row+1, col]
            world_list[row+1][col] = "P"
            world_list[row][col] = "/"
        else:
            location = [row, col]
    elif direction.upper() == "A" or direction == keys.LEFT:
        if world_list[row][col-1] != "#":
            location = [row, col-1]
            world_list[row][col-1] = "P"
            world_list[row][col] = "/" 
        else:
            location = [row, col]
    elif direction.upper() == "D" or direction == keys.RIGHT:
        if world_list[row][col+1] != "#":
            location = [row, col+1]
            world_list[row][col+1] = "P"
            world_list[row][col] = "/"
        else:
            location = [row, col]
    items["P"][0] = location
    return world_list, location, items

def update_ascii_map(world, row, col):
    """Updates the player position on the map"""
    pworld = []
    for i in range(len(world)):
        if i == row:
            pworld.append(world[row][:col]+"P"+world[row][col+1:])
        else:
            pworld.append(world[i])
    world = pworld
    return world

def map2dlist(world) -> list:
        """Converts the world map into a 2d list for easier collision detection and returns world_list"""
        world_list = []
        for i in range(len(world)):
            temp = list(world[i])
            world_list.append(temp)
        return world_list

def print_map(world):
    """Prints viewable map"""
    for i in range(len(world)):
        print(world[i])

def list2ascii(world_list):
    """Convert world_list back into ascii map """
    temp = []
    for i in range(len(world_list)):
        j = "".join(world_list[i])
        temp.append(j)
    return temp


"""Add remove_fog function"""
def remove_fog(map, items, location: list) -> list:
    """Pass the map and the coordinate of the player as a list. Returns a map with the fog of war removed for the 3x3 grid around the player."""
    
    # Finds the 3x3 grid around the player
    row, col = location
    clist = [[x, y] for x in range(location[0] - 1, location[0] + 2) for y in range(location[1] - 1, location[1] + 2)]
    
    new_map = [list(row) for row in map]

    # Removes the fog of war from the map
    for i, row in enumerate(new_map):
        for j, col in enumerate(row):
            new_map[i][j] = (" ") if (new_map[i][j] == "/" and [i, j] in clist) else (new_map[i][j])

    # Adds items onto map if discovered
    for item in items:
        locations = items[item]
        # Adds player to fog_world at location
        if item == "P":
            row, col = locations[0]
            new_map[row][col] = "P"
        # Adds other items to the map if discovered
        else:
            for i in range(len(items[item])):
                row, col = items[item][i]
                if new_map[row][col] not in "#/P":
                    new_map[row][col] = item

    # Converts the list back into the string
    map = ["".join(x) for x in new_map]
    
    return map

map_key = {
    "#": ":brick:",
    "/": ":cloud: ",
    "B": ":angry_face_with_horns:",
    "C": ":warning: ",
    "K": ":crown:",
    "L": ":heart_decoration:",
    "P": ":bust_in_silhouette:",
    "S": ":shopping_cart:",
    "H": ":bed: ",
    "E": ":chequered_flag:",
}
def emoji_map(map: "ASCII map") -> "emoji map":
    """Converts an ASCII map into an emoji map, then prints it to the screen"""
    em = []
    for row in range(len(map)):
        trow = ""
        for col in range(len(map[row])):
            symbol = map[row][col]
            if symbol in map_key.keys():
                symbol = emojize(map_key[symbol])
                if not(is_emoji(symbol) or is_emoji(symbol[:-1])):
                    symbol = emojize(":red_exclamation_mark:")
            elif symbol == " ":
                symbol = "  "
            else:
                symbol = emojize(":red_question_mark:")
            trow += symbol
        em.append(trow)
    return em

