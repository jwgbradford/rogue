import pygame as pg
import math, sys
import random as rnd

# set some constants for game sizes
HEIGHT = 20
WIDTH = 10
COLUMNS = 60
ROWS = 40

# set some constants for each colour (red, green, blue)
GREY, BLACK, WHITE = (150, 150, 150), (0, 0, 0), (255, 255, 255)
RED, YELLOW, BLUE= (255, 50, 50), (255, 255, 50), (50, 255, 50)
GREEN, BROWN = (50, 50, 255), (210,105,30)

class MyGame():
    # wrapper class for the game
    def __init__(self):
        pg.init()
        self.playing_area = pg.display.set_mode((COLUMNS * WIDTH, ROWS * HEIGHT))
        pg.display.set_caption('Rogue')
        self.clock = pg.time.Clock()
        rnd.seed()
        # blank list of rooms
        self.rooms = []
    
    def run(self):
        # generate a random level map
        self.playing_area.fill((0,0,0))
        self.map_rooms()
        self.current_room = rnd.choice(self.rooms)
        self.current_room.add_player()
        while True:
            for room in self.rooms:
                room.draw(self.playing_area)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.display.quit()
                    raise SystemExit
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        pass
                    # player goes up
                    elif event.key == pg.K_DOWN:
                        pass
                    elif event.key == pg.K_RIGHT:
                        pass
                    elif event.key == pg.K_LEFT:
                        pass
            pg.display.update()
            self.clock.tick(30)

    def map_rooms(self):
        # add one room to get things started
        size = (rnd.randint(3, 10), rnd.randint(3, 10))
        new_top_left = (rnd.randint(1, COLUMNS - size[0] - 1), rnd.randint(1, ROWS - size[1] - 1))
        self.rooms.append(Room(new_top_left, size))
        # now lets add more rooms, but check that they don't overlap
        num_of_rooms = 9 #rnd.randint(1, 6)
        for i in range(0, num_of_rooms):
            overlap = True
            while overlap:
                # default to no overlap
                overlap = False
                # make a temporary room parameters
                size = (rnd.randint(3, 10), rnd.randint(3, 10))
                new_top_left = (rnd.randint(1, COLUMNS - size[0] - 1), rnd.randint(1, ROWS - size[1] - 1))
                new_bottom_right = (new_top_left[0] + size[0], new_top_left[1] + size[1])
                # now check if if overlaps with any current rooms
                for existing_room in self.rooms:
                    if ((new_top_left[0] < existing_room.bottom_right[0] + 3 and new_top_left[1] < existing_room.bottom_right[1] +3) and 
                            (new_bottom_right[0] + 3 > existing_room.top_left[0] and new_bottom_right[1] + 3 > existing_room.top_left[1])):
                        overlap = True
            self.rooms.append(Room(new_top_left, size))
        passages = rnd.randint(num_of_rooms, num_of_rooms * 2)
        self.map_passages(passages)

    def map_passages(self, passages):
        # first lets figure out many doors on average our rooms should have
        door_ave = math.ceil(passages / len(self.rooms))
        room_dis = []
        for room in self.rooms:
            # need to find nearest room to this one
            # we start by finding the distance between rooms
            temp_distance = []
            for check_room in self.rooms:
                if room == check_room:
                    temp_distance.append(0)
                else:
                    temp_distance.append(self.range_check(room, check_room))
            room_dis.append(temp_distance)
        # now we can try and draw a line between closest rooms
        for room_count, room in enumerate(self.rooms):
            # we want the minimum distance, but each room is 0 away from itself
            # so we set it dist 999 to take it out of the equation
            # may be a 'neater' solution but can't think of it just now
            room_dis[room_count][room_count] = 999
            closest = 0
            for i, x in enumerate(room_dis[room_count]):
                if i != room_count:
                    if x == min(room_dis[room_count]):
                        closest = i
            pg.draw.line(self.playing_area, WHITE, 
                (room.top_left[0] * WIDTH, room.top_left[1] * HEIGHT), 
                (self.rooms[closest].bottom_right[0] * WIDTH, self.rooms[closest].bottom_right[1] * HEIGHT), 1)

    def range_check(self, room, check_room):
        # first we need to figure out if the check_room alignment
        # if our room is to the right of the check_room
        if room.top_left[1] - check_room.bottom_right[1] > 0:
            d_vert = room.top_left[1] - check_room.bottom_right[1]
        # else if our check_room is to the right of our room
        elif check_room.top_left[1] - room.bottom_right[1] >0:
            d_vert = check_room.top_left[1] - room.bottom_right[1]
        # else they overlap
        else:
            d_vert = 0
        # if our room is below the check_room
        if room.top_left[0] - check_room.bottom_right[0] > 0:
            d_hori = room.top_left[0] - check_room.bottom_right[0]
        # else if our check_room is below our room
        elif check_room.top_left[0] - room.bottom_right[0] > 0:
            d_hori = check_room.top_left[0] - room.bottom_right[0]
        # else they overlap
        else:
            d_hori = 0
        distance = d_vert + d_hori
        return distance

class Room():
    # object for storing groups of tiles as a room
    def __init__(self, top_left, size):
        # our first room can go anywhere
        # but we'll start in the top left
        self.top_left = top_left
        self.bottom_right = (self.top_left[0] + size[0] , self.top_left[1] + size[1])
        self.room_tiles = self.build_room(size)

    def build_room(self, size):
        length, height = size
        room_tiles = []
        for column in range(0, length):
            room_tiles.append([])
            for row in range(0, height):
                room_tiles[column].append([])
                if row == 0 or row == height -1:
                    # top and bottom walls
                    room_tiles[column][row].append(Wall('horizontal'))
                elif column == 0 or column == length -1:
                    # side walls
                    room_tiles[column][row].append(Wall('vertical'))
                # need to add corner designs
                else:
                    #middle
                    room_tiles[column][row].append(Floor())
        return room_tiles

    def add_doors(self, room_tiles, size):
        doors = rnd.randint(1, 16)
        doors_bin = self.convert_to_binary(doors)
        if doors_bin[0] == '1':
            pos = rnd.randint(1, size[1] - 1)
            room_tiles[size[0] - 1][pos].append(Wall('horizontal'))
        if doors_bin[1] == '1':
            pos = rnd.randint(1, size[1] - 1)
            room_tiles[0][pos].append(Wall('horizontal'))
        if doors_bin[2] == '1':
            pos = rnd.randint(1, size[0] - 1)
            room_tiles[pos][size[1] - 1].append(Wall('vertical'))
        if doors_bin[3] == '1':
            pos = rnd.randint(1, size[0] - 1)
            room_tiles[pos][0].append(Wall('vertical'))
        return room_tiles

    def convert_to_binary(self, doors):
        doors_dec = doors
        doors_bin  = [0, 0, 0, 0]
        if doors_dec % 2 == 1:
            doors_bin[3] = '1' # North
            doors_dec -= 1
        if doors_dec % 2 == 0 and doors_dec > 0:
            doors_bin[2] = '1' # South
            doors_dec -= 2
        if doors_dec % 4 == 0 and doors_dec > 0:
            doors_bin[1] = '1' # East
            doors_dec -= 4
        if doors_dec % 8 == 0 and doors_dec > 0:
            doors_bin[0] = '1' # West
            doors_dec -= 8
        return doors_bin

    def draw(self, playing_area):
        for column_num, column in enumerate(self.room_tiles):
            for row_num, tile in enumerate(column):
                # draw the tile, -1 in a list is always the last item
                tile[-1].draw(playing_area, (self.top_left[0] + column_num) * WIDTH, (self.top_left[1] + row_num) * HEIGHT)

    def add_player(self):
        start_column = int((self.bottom_right[0] - self.top_left[0]) / 2)
        start_row = int((self.bottom_right[1] - self.top_left[1]) / 2)
        # let's create a player object
        self.player = Player()
        # and then store them in our room
        self.room_tiles[start_column][start_row].append(self.player)

    def move_player(self, dir):
        if dir == 'up':
            pass

class Tile():
    # parent class for everthing in the game
    def __init__(self):
        # height & width of a tile
        self.height = HEIGHT
        self.width = WIDTH
        self.image = self.make_object_surface()
        self.rect = self.image.get_rect()

    def make_object_surface(self): #returns a surface that is a square of size and colour
        surface = pg.Surface((self.width, self.height))
        # start with a black background
        surface.fill(BLACK)
        # then add the icon / design for the tile
        self.draw_icon(surface)
        return surface

    def draw(self, playing_area, x, y): # updates playing_area with self's image and population
        playing_area.blit(self.image, (x, y))

class Floor(Tile):
    # our basic floor tile
    def __init__(self):
        super().__init__()

    def draw_icon(self, surface):
        # a simple dot for the floor
        pg.draw.circle(surface, BROWN, (self.width / 2, self.height / 2), self.width / 4, 0)

class Wall(Tile):
    # our basic wall tile, has orientation
    def __init__(self, dir):
        self.dir = dir
        super().__init__()

    def draw_icon(self, surface):
        if self.dir == 'vertical':
            pg.draw.rect(surface, BROWN, (2, 0, 3, 20))
            pg.draw.rect(surface, BROWN, (7, 0, 9, 20))
        elif self.dir == 'horizontal':
            pg.draw.rect(surface, BROWN, (0, 4, 10, 6))
            pg.draw.rect(surface, BROWN, (0, 14, 10, 18))
        elif self.dir == 'top_right':
            pass

class Player(Tile):
    # our basic character tile, has movement
    def __init__(self):
        super().__init__()

    def draw_icon(self, surface):
        # simple dot for our player
        pg.draw.circle(surface, BLUE, (self.width / 2, self.height / 2), self.width / 2, 0)

if __name__ == "__main__":
    my_game = MyGame()
    my_game.run()