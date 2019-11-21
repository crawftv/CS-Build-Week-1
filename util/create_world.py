from django.contrib.auth.models import User
from adventure.models import Player, Room, Item, Monster

Room.objects.all().delete()
Item.objects.all().delete()
Monster.objects.all().delete()

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
            room = Room(title="A Generic Room", description="This is a generic room.",)
            # Note that in Django, you'll need to save the room after you create it
            room.save()

            # Save the room in the World grid
            self.grid[y][x] = room

            # Connect the new room to the previous room
            opposite_dictionary = {"w": "e", "e": "w", "s": "n", "n": "s"}
            if previous_room is not None:
                print(room, room_direction)
                previous_room.connect_rooms(room, room_direction)
                print(previous_room, opposite_dictionary[room_direction])
                room.connect_rooms(previous_room, opposite_dictionary[room_direction])

            # Update iteration variables
            previous_room = room
            room_count += 1

    def print_rooms(self):
        """
        Print the rooms in room_grid in ascii characters.
        """  # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"
        # The console prints top to bottom but our array is arranged # bottom to top.
        # # We reverse it so it draws in the right direction.  reverse_grid = list(self.grid)
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


players = Player.objects.all()
world = World()
world.generate_rooms(10, 10, 100)
first_room = world.grid[0][0]

for p in players:
    p.currentRoom = first_room.id
    p.save()

gold = Item.objects.create(name="gold", level=1)

m_spider = Monster.objects.create(name="Frost Spider", level=1, hp=5, ad=1)
m_spider.inventory.set([gold, gold])
print("World Created")
r = Room.objects.all()
for i in r[0:20]:
    print(
        {
            "id": i.id,
            "title": i.title,
            "description": i.description,
            "n_to": i.n_to,
            "s_to": i.s_to,
            "e_to": i.e_to,
            "w_to": i.w_to,
        }
    )
