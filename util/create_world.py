from django.contrib.auth.models import User
from adventure.models import Player, Room, Item, Monster
import random

# Reset World
Room.objects.all().delete()
Item.objects.all().delete()
Monster.objects.all().delete()
# Create monsters and items
base_items = ["staff", "dagger", "sword", "axe"]
l1_adj = ["ancient", "rusty", "broken"]
l5_adj = ["mighty", "arcane", "dwarven"]
items = [None] * 80
for i in range(15):
    s = f"{random.choice(l1_adj)} {random.choice(base_items)}"
    item = Item.objects.create(name=s, level=1, description="")
    item.save()
    items.append(item)

for i in range(5):
    s = f"{random.choice(l5_adj)} {random.choice(base_items)}"
    item = Item.objects.create(name=s, level=1, description="")
    item.save()
    items.append(item)

random.shuffle(items)

gold = Item.objects.create(name="gold", level=1)
m_spider = Monster.objects.create(name="Frost Spider", level=1, hp=5, ad=1)
m_spider.inventory.set([gold])
# Create World class
class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms):
        """
        Fill up the grid, bottom to top, in a zig-zag pattern
        """

        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x

        # Start from lower-left corner (0,0)
        x = -1  # (this will become 0 on the first step)
        y = 0
        room_count = 0

        # Start generating rooms to the east
        direction = 1  # 1: east, -1: west

        p_adj = ["Frozen", "Frostbit", "Shivering", "Glacial"]
        h_c_adj = [
            "Desolate",
            "Bleak",
            "Dreary",
            "Bare",
            "Deserted",
            "Forlorn",
            "Gloomy",
            "Barren",
            "Bereft",
        ]
        r_adj = ["Warm", "Cozy"]
        cryptic_adj = ["Cryptic", "Dark", "Dim", "Mysterious"]

        h = [f"{random.choice(h_c_adj+cryptic_adj)} {i}" for i in ["Hallway"] * 40]
        p = [f"{random.choice(p_adj+cryptic_adj)} {i}" for i in ["Pass"] * 15]
        c = [f"{random.choice(h_c_adj+cryptic_adj)} {i}" for i in ["Chamber"] * 15]
        cell = [f"{random.choice(h_c_adj+cryptic_adj)} {i}" for i in ["Cell"] * 15]
        room = [f"{random.choice(cryptic_adj)} {i}" for i in ["Room"] * 15]
        names = h + p + c + cell + room

        # While there are rooms to be created...
        previous_room = None
        while room_count < num_rooms:

            # Calculate the direction of the room to be created
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1

            # Create a room in the given direction

            name = random.choice(names)
            names.pop(names.index(name))
            room = Room(title=name, description="This is a generic room.", x=x, y=y)
            room.save()
            item = items.pop()
            if item is not None:
                room.inventory.set([item])
            # Note that in Django, you'll need to save the room after you create it

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            opposite_dictionary = {"w": "e", "e": "w", "s": "n", "n": "s"}
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)
                room.connect_rooms(previous_room, opposite_dictionary[room_direction])

            # Update iteration variables
            previous_room = room
            room_count += 1

    def add_random_connections(self):
        for i in range(0, self.height, 2):
            for j in range(0, self.width):
                if random.randint(0, 1) == 1:
                    world.grid[i][j].connect_rooms(world.grid[i + 1][j], "n")
                    world.grid[i + 1][j].connect_rooms(world.grid[i][j], "s")

    def print_rooms(self):
        """
        Print the rooms in room_grid in ascii characters.
        """  # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"
        # The console prints top to bottom but our array is arranged # bottom to top.
        # # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)
        # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


world = World()
world.generate_rooms(10, 10, 100)
world.add_random_connections()
first_room = world.grid[0][0]
world_map = Item.objects.create(
    name="Map", description="A map of you environment", level=1
)
first_room.inventory.set([world_map])
players = Player.objects.all()
for p in players:
    p.currentRoom = first_room.id
    p.save()

print("World Created")
