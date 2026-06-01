
import pgzrun
import random
import pygame

WIDTH = 1398
HEIGHT = 766

mapdeviation=0

positions =[250,500,750,1000,1250,1875*2,1750*2,1625*2,1500*2,1375*2,1250*2,1125*2,1000*2,875*2,750*2,625*2,500*2,375*2,250*2]

rows = 14
columns = 5

path = []
path_information = []
drawn_positions = []
special_locations = random.sample(range(1,14), 5)
location_shops = special_locations[:3]
location_elites = special_locations[3:]

start = random.randint(0, columns)

for row in range(rows):
    path_information.append((start,row))
    x = random.randint(start-1, start +1)
    if x>4:
        x = 4
    if x<0:
        x = 0

for i in range(rows):
    path.append((positions[path_information[i][0]],positions[path_information[i][1]+5]))
print(location_elites, location_shops)
path.append((700,250))

map = Actor('map.png')
map.x = WIDTH/2
map.bottom = HEIGHT

for positions in path:
    if path.index(positions) in location_shops:
        location = Actor('shop.png')
        location.type = 'shop'
        location.layer = path.index(positions)
    elif path.index(positions) in location_elites:
        location = Actor('elite.png')
        location.type = 'elite'
    elif path.index(positions) == 14:
        location = Actor('boss.png')
        location.type = 'boss'
        location.layer = path.index(positions)
    else:
        location = Actor('enemy.png')
        location.type = 'enemy'
        location.layer = path.index(positions)
    location.pos = positions
    drawn_positions.append(location)

for position in drawn_positions:
    position.y -=3200

def draw():
    map.draw()
    

    for i in range(14):
        pygame.draw.line(screen.surface, "black",
                     (path[i][0],path[i][1]-3200+mapdeviation), (path[i + 1][0],path[i + 1][1]-3200+mapdeviation), 5)

    for position in drawn_positions:
        position.draw()

def update():
    global x
    if keyboard.w:
        map.y += 10
        for position in drawn_positions:
            position.y += 10 
        x += 10  
    if keyboard.s:
        map.y -= 10
        for position in drawn_positions:
            position.y -= 10
        x -= 10


pgzrun.go()
