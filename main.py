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
        # create a player object in the game
        self.player = Player()
        self.current_room.add_player(self.player)
        while True:
            for room in self.rooms:
                room.draw(self.playing_area)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.display.quit()
                    raise SystemExit
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP or event.key == pg.K_DOWN or event.key == pg.K_RIGHT or event.key == pg.K_LEFT:
                        self.current_room.move_player(self.player, event.key)
            pg.display.update()
            self.clock.tick(10)

    def map_rooms(self):
        # add one room to get things started
        size = (rnd.randint(3, 10), rnd.randint(3, 10))
        new_top_left = (rnd.randint(1, COLUMNS - size[0] - 1), rnd.randint(1, ROWS - size[1] - 1))
        self.rooms.append(Room(new_top_left, size))
        # now lets add more rooms, but check that they don't overlap
        num_of_rooms = 6 #rnd.randint(1, 6)
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
        # come back to mapping passages later
        #self.map_passages(passages)

    def map_passages(self, passages):
        # work out distances between all our rooms
        room_distance_lists = self.calculate_distances()
        print(room_distance_lists)
        # our starting room = 0 is always on the path
        path_list = [0]
        # on our first pass we just want to connect all the rooms once
        # we start with the first room in the list

# we have a list of lists, called room_distance_lists. Each list represents a room. Each room has a list of distances to the other rooms
# we iterate over the first list (of rooms)
# for each room, we want the closest room to that room
# if we're not already connected to that room, we connect and make the reciprocal link
# if we are connected to that room
# if there is are more than room the same distance, we try them first
# if not, we go to the next nearest room
# once we have one connection, we move to the next room/ list

        room_being_checked = 0
        for count in range(len(self.rooms)):
            not_connected = True
            closeness = 1 # closeness = 0 would be same room
            while not_connected:
                list_of_closest_rooms = self.find_nearest_room(room_distance_lists[room_being_checked], closeness)
                # now check if any of the closest_index rooms are connected to our rooms_being_checked
                for closest_index in range(len(list_of_closest_rooms)):
                    if list_of_closest_rooms[closest_index] not in self.rooms[room_being_checked].connected_rooms:
                        #add our closest_index room to the one being checked
                        self.rooms[room_being_checked].connected_rooms.append(list_of_closest_rooms[closest_index])
                        # we also need to add the reciprical
                        self.rooms[list_of_closest_rooms[closest_index]].connected_rooms.append(room_being_checked)
                        # and we add this newly connected room to our path_list
                        print(room_being_checked, 'is connected to', list_of_closest_rooms[closest_index])
                        path_list.append(room_being_checked)
                        # and set our new room_being_checked as the one we've just connected to
                        room_being_checked = list_of_closest_rooms[closest_index]
                        not_connected = False
                        break # we found our closest room, move on
                    # we didn't find our closest room, move to next closest
                closeness += 1

        for room in self.rooms:
            print(room.connected_rooms)
#            pg.draw.line(self.playing_area, WHITE, 
#                (room.top_left[0] * WIDTH, room.top_left[1] * HEIGHT), 
#                (self.rooms[room.connected_rooms[0]].bottom_right[0] * WIDTH, self.rooms[room.connected_rooms[0]].bottom_right[1] * HEIGHT), 1)

    def calculate_distances(self):
        room_dis = []
        for room in self.rooms: 
            # need to find closest_index room to this one
            # we start by finding the distance between rooms
            temp_distance = []
            for check_room in self.rooms:
                if room == check_room:
                    temp_distance.append(0)
                else:
                    dist = self.range_check(room, check_room)
                    temp_distance.append(dist)
            room_dis.append(temp_distance)
        return room_dis

    def find_nearest_room(self, unordered_list, required_index):
        sorted_list = sorted(unordered_list)
        distance = sorted_list[required_index]
        distances = [i for i, e in enumerate(unordered_list) if e == distance]
        return distances

        '''
        closest_index = 0
        keep_checking = True
        while keep_checking:
            # we want the minimum distance, but each room is 0 away from itself
            # so we set it dist 999 to take it out of the equation
            room_dis[closest_index][closest_index] = 999
            closest_index = 0
            for i, x in enumerate(room_dis[closest_index]):
                if i != closest_index:
                    if x == min(room_dis[closest_index]):
                        # the closest_index room to this room is i
                        closest_index = i
            if closest_index not in room.connected_rooms:
                room.connected_rooms.append(closest_index)
                # we also need to add the reciprical
                self.rooms[closest_index].connected_rooms.append(closest_index)
                # and we add this newly connected room to our path_list
                path_list.append(closest_index)
                room_num = closest_index
            else: # our rooms are already connected
                # we need to check each other room distance until we either find one not in path_list
                # or we run out of rooms, and have reached the end of the first pass path
                # but need a way of finding next min distance room in list
                pass
            if len(path_list) == len(self.rooms):
                keep_checking = False
        # need a different strategy at this point - start with self.current_room
        # then iterate through list finding nearest_room

        for closest_index, room in enumerate(self.rooms):
            # we want the minimum distance, but each room is 0 away from itself
            # so we set it dist 999 to take it out of the equation
            room_dis[closest_index][closest_index] = 999
            closest_index = 0
            for i, x in enumerate(room_dis[closest_index]):
                if i != closest_index:
                    if x == min(room_dis[closest_index]):
                        # the closest_index room to this room is i
                        closest_index = i
            # now we check if we're already connected to room 'i'
            if closest_index not in room.connected_rooms:
                room.connected_rooms.append(closest_index)
                # we also need to add the reciprical
                self.rooms[closest_index].connected_rooms.append(closest_index)
                # and we add this newly connected room to our path_list
                path_list.append(closest_index)
            else: # our rooms are already connected
                # we need to check each other room distance until we either find one not in path_list
                # or we run out of rooms, and have reached the end of the first pass path
                # but need a way of finding next min distance room in list

        '''


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
        # we need to keep a list of which rooms 'this' room is connected to
        self.connected_rooms = []

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

    def add_player(self, player):
        start_column = int((self.bottom_right[0] - self.top_left[0]) / 2)
        start_row = int((self.bottom_right[1] - self.top_left[1]) / 2)
        # lets give our player their starting coordinates
        player.column = start_column
        player.row = start_row
        # and then store them in our room
        self.room_tiles[start_column][start_row].append(player)

    def move_player(self, player, event_key):
        # check our player can move in the chosen direction
        move = False
        if event_key == pg.K_UP and isinstance(self.room_tiles[player.column][player.row - 1][-1], Floor):
            new_row = player.row - 1
            new_column = player.column
            move = True
        elif event_key == pg.K_DOWN and isinstance(self.room_tiles[player.column][player.row + 1][-1], Floor):
            new_row = player.row + 1
            new_column = player.column
            move = True        
        elif event_key == pg.K_RIGHT and isinstance(self.room_tiles[player.column + 1][player.row][-1], Floor):
            new_row = player.row
            new_column = player.column + 1
            move = True        
        elif event_key == pg.K_LEFT and isinstance(self.room_tiles[player.column - 1][player.row][-1], Floor):
            new_row = player.row
            new_column = player.column - 1
            move = True       
        if move:
            self.room_tiles[player.column][player.row].remove(player)
            self.room_tiles[new_column][new_row].append(player)
            player.column = new_column
            player.row = new_row

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