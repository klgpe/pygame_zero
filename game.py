import pgzrun
import random
import pygame
import math
from pygame import Rect
from pygame.math import Vector2
import os
import sys
import time

WIDTH = 1398
HEIGHT = 766
MOVESPEED = 9
JUMP_SPEED = 24
GRAVITY = 0.8
MAX_FALL_SPEED = 30
BULLET_SPEED = 30
DIRECTION = 1
vx = 0
vy = 0
CAMERA_X =0
CAMERA_Y =0
ATTACKCOOLDOWN_SANDWORMS = 200
current_layer = 0
map_on = True
mapdeviation=0
mapdeviationx=-3000
rows = 14
columns = 5
current_position = None
tree_alive = False
boss_alive = False
angle = 0
gold = 0
reward_screen = False
game_over = False
shop_open = False
victory_screen = False

#rotes overlay bei viel damage:
red_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
alpha = 80
red_overlay.fill((255, 0, 0, alpha))  # Rot, Alpha=80

#gegner
enemies=[]

#enemy bullets#
enemy_bullets=[]

#map positionen
positions =[250,500,750,1000,1250,1875*2,1750*2,1625*2,1500*2,1375*2,1250*2,1125*2,1000*2,875*2,750*2,625*2,500*2,375*2,250*2]
path = []
path_information = []
drawn_positions = []
special_locations = random.sample(range(1,14), 7)
location_shops = special_locations[:3]
location_elites = special_locations[3:]
finished_loc = []

leafs = []

start = random.randint(0, columns-1)
start1 = random.randint(0, columns-1)
start2 = random.randint(0, columns-1)

for row in range(rows):
    path_information.append(((start,start1,start2),row))
    start = random.randint(start-1, start +1)
    start1 = random.randint(start1-1, start1+1)
    start2 = random.randint(start2-1, start2+1)

    if start>4:
        start = 4
    if start<0:
        start = 0
    if start1 >4:
        start1 = 4
    if start1<0:
        start1 = 0
    if start2 >4:
        start2 = 4
    if start2<0:
        start2 = 0  

for i in range(rows):
    path.append(((positions[path_information[i][0][0]],positions[path_information[i][0][1]],positions[path_information[i][0][2]]),positions[path_information[i][1]+5]))
path.append(((700,700,700),250))
map = Actor('map.png')

for position in path:
    for different in path[path.index(position)][0]:
        if path.index(position) in location_shops and random.randint(1,2) == 1 and (not drawn_positions or (different,position[1]) != drawn_positions[max(len(drawn_positions)-1,0)].pos and (different,position[1]) != drawn_positions[max(len(drawn_positions)-2,len(drawn_positions)-1,0)].pos):
            location = Actor('shop.png')
            location.type = 'shop'
            location.layer = path.index(position)
        elif path.index(position) in location_elites and random.randint(1,2) == 1 and (not drawn_positions or (different,position[1]) != drawn_positions[max(len(drawn_positions)-1,0)].pos and (different,position[1]) != drawn_positions[max(len(drawn_positions)-2,len(drawn_positions)-1,0)].pos):
            location = Actor('elite.png')
            location.type = 'elite'
            location.layer = path.index(position)
        elif path.index(position) == 14:
            location = Actor('boss.png')
            location.type = 'boss'
            location.layer = path.index(position)
        elif not drawn_positions or ((different,position[1]) != drawn_positions[max(len(drawn_positions)-1,0)].pos and (different,position[1]) != drawn_positions[max(len(drawn_positions)-2,len(drawn_positions)-1,0)].pos):
            location = Actor('enemy.png')
            location.type = 'enemy'
            location.layer = path.index(position)
        location.pos = (different,position[1])
        drawn_positions.append(location)




#platformen in Listen
platforms = [Actor("platform0"),Actor("platform1"),Actor("platform2"),Actor("platform3"),Actor("platform0"),Actor("platform1"),Actor("platform2"),Actor("platform3")]
platform_pos_topleft = [(700,270),(900, -50), (1550,200),( 1900, 50),(300,220),(500, -10), (1500, -100),(1100, 300),(2000,220)]
platform_draw = []

tree_images = ["tree0","tree1","tree2","tree3"]
#animationen
walk_frames = ["mage_walk1","mage_walk2",'mage_walk5',"mage_walk4", "mage_walk_reverse1","mage_walk_reverse2",'mage_walk_reverse5',"mage_walk_reverse4"]
idle_frames = ['mage_idle0','mage_idle1','mage_idle2','mage_idle3','mage_idle4','mage_idle_reverse0','mage_idle_reverse1','mage_idle_reverse2','mage_idle_reverse3','mage_idle_reverse4']
fire_ball_frames = ['fireball0','fireball1','fireball2']
explotion_frames =['explosion0','explosion1','explosion2','explosion3','explosion4']
sandwurm_frames = ['sandwurm_up0','sandwurm_up1','sandwurm_up2','sandwurm_up3','sandwurm_up4','sandwurm_up5','sandwurm_up6','sandwurm_down0','sandwurm_down1','sandwurm_down2','sandwurm_down3','sandwurm_down4','sandwurm_down5','sandwurm_dowm6']
fly_frames =['fly_left0','fly_left1','fly_left2','fly_left3','fly_left4','fly_right0','fly_right1','fly_right2','fly_right3','fly_right4']


FRAME_INDEX_WALK = 0
FRAME_INDEX_IDLE = 0 
SPEED = 8
WALK_ANIMATION = SPEED
IDLE_ANIMATION = SPEED +2

#camera verschiebung
def camera(pos):
    x, y = pos
    return (x - CAMERA_X, y - CAMERA_Y)

#backround
bg = Actor('background.png', topleft=(0,-300))

#untergrund
ground = Actor('untergrund.png', topleft=(0,00))

#character  
mc = Actor('mage.png',midbottom=(704,623))
mc.max_hp = 100
mc.hp = 100
mc.regeneration = 0
mc.damage_bonus = 0

def tree():
    global tree_alive
    tree = Actor('tree0.png')
    tree.image = tree_images[random.randint(0,3)]
    tree.type = 'tree'
    tree.hp = 100 + 20*current_layer
    tree.pos = (1450, 265)
    tree.damage = False
    tree_alive = True
    enemies.append(tree)

def boss():
    global boss_alive
    boss = Actor('boss1.png')
    boss.type = 'boss'
    boss.hp = 1000
    boss.pos = (1450, 300)
    boss.bottom = 700
    boss.damage = False
    boss_alive = True
    enemies.append(boss)

#fire_bullet
bullets = []
explotions =[]

mc.stand = True
mc.on_g = True
shop_draw=[]
def shop():
    global shop_open

    shop_open = True
    shopbg = Actor('shopbg.png')
    shop.bottom = HEIGHT
    shop.x = WIDTH/2
    shop_draw.append(shopbg) 

#platformen und orte (indexe) auswählen
def platforminformation():
    return random.sample(range(8), 5 )+ random.sample(range(9), 5)
#platformen und positionen werden anhand von indexen rausgesucht und die platformen dann in eine liste zusammen gefügt
def platformlist(list):
    platform_draw_setup = []
    
    #5 platformen pro stage
    
    for platform_index in range(5):
        
        #platform desing wird rausgesucht
        actor = platforms[list[platform_index]]
        
        #platformposition wird zugeordnet
        actor.topleft = platform_pos_topleft[list[platform_index + 5]]
        
        #platform wird an liste gefügt 
        platform_draw_setup.append(actor)
    
    return platform_draw_setup 

connections = []


for row in range(rows-1):

    current = path_information[row]
    nxt = path_information[row+1]

    for i in range(3):
        connections.append(
            (
                (current[0][i], current[1]),
                (nxt[0][i], nxt[1])
            )
        )

def launch(type):
    
    global platform_draw, enemies, current_layer, shop_open, victory_screen
    if type == 'enemy':
        #lsite mit echten platformen erstelen
        platform_draw = []
        platform_draw = platformlist(platforminformation())
        #startposition der platformen merken
        #sandwürmer spawnen
        current_layer += 1
        sandwurm(random.randint(max(2,current_layer-7),max(1,current_layer*2)))
        fly(random.randint(max(2,current_layer-7),max(0,current_layer*2)))
    if type == 'elite':
        platform_draw = []
        platform_draw = platformlist(platforminformation())
        current_layer += 1
        tree()
    if type == 'boss':
        platform_draw = []
        platform_draw.append(Actor('platform0.png',(400,300)))
        platform_draw.append(Actor('platform0.png',(2300,300)))
        current_layer += 1
        boss()
    if type == 'shop':
    
        current_layer += 1
        shop_open = True
def leaf1(anzahl):
    global leafs
    for i in range(anzahl):
        leaf = Actor ('leaf.png')
        leaf.angle = i
        leaf.pos = ( 1000,500)
        leafs.append(leaf)

def fly(anzahl):
    for i in range(anzahl):
        fly = Actor('fly_left0')
        fly.type = 'fly'
        fly.pos = (random.randint(1000,2000),random.randint(400,500))
        fly.hp = 10
        fly.speed =4
        fly.direction = 1
        fly.timer = random.randint(0,500) #timer
        fly.angle = random.uniform(0,720)
        fly.damage  = False
        enemies.append(fly)


#sandwurm gegner
def sandwurm(anzahl):
    for i in range(anzahl):

        x = random.randint(0, 4)

        worm = Actor("sandwurm_up6")
        worm.pos = (platform_draw[x].x, platform_draw[x].top )

        worm.type = "sandwurm"
        worm.frame_index = 0
        worm.timer = random.randint(0, 100)
        worm.hp = 20
        worm.state = 'empty'
        worm.animationdelay =0
        worm.damage = False
        
        enemies.append(worm)





#feuerbälle schießen
def on_mouse_down(pos):
    global map_on, finished_loc, positions, current_position, victory_screen
    if map_on == True:
        for position in drawn_positions:
            hitbox = Rect(position.left+mapdeviationx, position.top -3200 +250*max(0,current_layer)+mapdeviation, position.width, position.height)
            
            if hitbox.collidepoint(pos) and current_position is None:
                print("geklickt:", position.type, position.layer)
                if position.type == 'shop'and position.layer == current_layer :
                    launch('shop')
                elif position.type == 'elite'and position.layer == current_layer :
                    launch('elite')
                elif position.type == 'enemy'and position.layer == current_layer:
                    launch('enemy')
                elif position.type == 'boss' and position.layer == current_layer:
                    launch('boss')
                map_on = False
                finished_loc.append(position.pos)
                current_position = position.pos
                return
            elif hitbox.collidepoint(pos) and current_position is not None:
                allowed = False

                for start, end in connections:

                    start_pos = (positions[start[0]],positions[start[1] + 5])
                    end_pos = (positions[end[0]],positions[end[1] + 5])

                    if start_pos == current_position:
                        if (position.x, position.y) == end_pos:
                            allowed = True
                            break

                if not allowed and current_layer < 14:
                    return
                print("geklickt:", position.type, position.layer)
                if position.type == 'shop'and position.layer == current_layer :
                    launch('shop')
                elif position.type == 'elite'and position.layer == current_layer :
                    launch('elite')
                elif position.type == 'enemy'and position.layer == current_layer:
                    launch('enemy')
                elif position.type == 'boss' and position.layer == current_layer :
                    launch('boss')
                map_on = False
                finished_loc.append(position.pos)
                current_position = position.pos
                return
    
    else:
        bullet = Actor('fireball0.png')
        bullet.pos = (mc.x+50,mc.y+30)
        # 2d Vector erstellen zwischen 
        world_mouse = Vector2(pos[0] + CAMERA_X,
                          pos[1] + CAMERA_Y)
        direction = world_mouse - Vector2(mc.x + 50,mc.y + 30)
        #verktor mit länge 1 berechnen - feuer fliegt immer gleich schnell
        if direction.length() != 0: 
            direction = direction.normalize()
        #daraus tatsächlich überquerte distanz in 1 tick berechen
        bullet.velocity = direction * BULLET_SPEED
        #zielposition zwischenspeichern
        bullet.target = world_mouse

        #animation
        bullet.frame_index = 0

        bullets.append(bullet)

#enemy_shoot
def enemy_shoot(pos):
        bullet = Actor('enemy_bullet.png')
        bullet.pos = pos

        direction = Vector2(mc.x, mc.y+50) - Vector2(pos)

        if direction.length() != 0:
            direction = direction.normalize()

        bullet.velocity = direction * 8

        enemy_bullets.append(bullet)

def map1():
    global map_on , mapdeviationx, current_layer   
    
    mapdeviationx = 0
    map.bottom = HEIGHT +150*max(0,current_layer)
    map.x = WIDTH/2
    map_on = True

def level_complete():
    global reward_screen, gold

    gold += 10
    reward_screen = True

#kamera funktion
def camera(pos):
    x, y = pos
    return (x - CAMERA_X, y - CAMERA_Y)

def draw():
    global map_on , mapdeviationx, current_layer , finished_loc, tree_alive, boss_alive, leafs, victory_screen
 # Hintergrund
    screen.blit(bg.image,(bg.left - CAMERA_X * 0.5, bg.top - CAMERA_Y * 0.5))

    

    # Plattformen
    for platform in platform_draw:
        screen.blit(platform.image,camera(platform.topleft))

    #gegner
    for enemy in enemies:
        screen.blit(enemy.image, camera(enemy.topleft))
    # Boden
    screen.blit(ground.image,camera(ground.topleft))
    # Bullets
    for bullet in bullets:
        screen.blit(bullet.image,camera(bullet.topleft))

    # Spieler
    screen.blit(mc.image, camera(mc.topleft))  

    for leaf in leafs:
        screen.blit(leaf.image,camera(leaf.topleft))
    
    # Explosionen
    for explotion in explotions:
        screen.blit(explotion.image,camera(explotion.topleft))
    
    #bullet from enemy
    for bullet in enemy_bullets:
        screen.blit(bullet.image,camera(bullet.topleft))

    # Hintergrund
    screen.draw.filled_rect(Rect((20, 20), (300, 30)), (60, 60, 60))

    # Aktuelle HP
    breite = 300 * mc.hp / mc.max_hp
    screen.draw.filled_rect(Rect((20, 20), (breite, 30)), (255, 0, 0))

    # Rahmen
    pygame.draw.rect(screen.surface,(255, 255, 255),Rect((20, 20), (300, 30)),6  )
    #rotes overlay
    if mc.damage == True:
        alpha = random.randint(70, 90)
        red_overlay.fill((255, 0, 0, alpha))
        screen.surface.blit(red_overlay, (0, 0))
    if not mc.damage == True:
        red_overlay.fill((255, 0, 0, 0))
        screen.surface.blit(red_overlay, (0, 0))
    
    screen.draw.text(
        f"G: {gold}",
        topleft=(20, 60),
        fontsize=20,
        fontname="pixel",
        color="yellow",
        owidth=2,
        ocolor="black"
    )   

    map.draw()
    for i in range(14):
        pygame.draw.line(screen.surface, "black",
                     (path[i][0][0]+mapdeviationx,path[i][1]-3200+250*max(0,current_layer)+mapdeviation), (path[i + 1][0][0]+mapdeviationx,path[i + 1][1]-3200+250*max(0,current_layer)+mapdeviation), 3)
    
   
    for i in range(14):
        pygame.draw.line(screen.surface, "black",
                     (path[i][0][1]+mapdeviationx,path[i][1]-3200+250*max(0,current_layer)+mapdeviation), (path[i + 1][0][1]+mapdeviationx,path[i + 1][1]-3200+250*max(0,current_layer)+mapdeviation), 3)

    
    for i in range(14):
        pygame.draw.line(screen.surface, "black",
                     (path[i][0][2]+mapdeviationx,path[i][1]-3200+250*max(0,current_layer)+mapdeviation), (path[i + 1][0][2]+mapdeviationx,path[i + 1][1]-3200+250*max(0,current_layer)+mapdeviation), 3)

    for locs in finished_loc:
         pygame.draw.line(screen.surface, "black",
                     (locs[0]+mapdeviationx,locs[1]-3200+250*max(0,current_layer)+mapdeviation), (finished_loc[min(finished_loc.index(locs)+1,len(finished_loc)-1)][0]+mapdeviationx,finished_loc[min(finished_loc.index(locs)+1,len(finished_loc)-1)][1]+mapdeviationx-3200+250*max(0,current_layer)+mapdeviation), 15)


    for position in drawn_positions:
        screen.blit(position.image,( position.left+mapdeviationx , position.top -3200 +250 * max(0,current_layer)+mapdeviation))

    if shop_open:

        screen.blit("shopbg", (0, -100))

        screen.draw.text(
            f"Gold: {gold}",
            center=(700, 50),
            fontsize=30,
            fontname="pixel",
            color="yellow",
            owidth=2,
            ocolor="black"
        )

        screen.draw.text(
            "ESC = Zur Karte",
            center=(700, 740),
            fontsize=18,
            fontname="pixel",
            color="yellow"
        )

    

    # Belohnungsfenster
    if reward_screen:

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.surface.blit(overlay, (0, 0))

        pygame.draw.rect(
            screen.surface,
            (230, 200, 120),
            Rect((WIDTH//2 - 250, HEIGHT//2 - 100), (500, 200))
        )

        pygame.draw.rect(
            screen.surface,
            (0, 0, 0),
            Rect((WIDTH//2 - 250, HEIGHT//2 - 100), (500, 200)),
            5
        )

        screen.draw.text(
            "Level abgeschlossen!",
            center=(WIDTH//2, HEIGHT//2 - 40),
            fontsize=20,
            fontname="pixel",
            color="black"
        )

        screen.draw.text(
            "Du hast 10 Gold erhalten!",
            center=(WIDTH//2, HEIGHT//2 + 10),
            fontsize=15,
            fontname="pixel",
            color="black"
        )

        screen.draw.text(
            "ESC -> Zur Karte",
            center=(WIDTH//2, HEIGHT//2 + 60),
            fontsize=15,
            fontname="pixel",
            color="black"
        )

    if game_over:

        # dunkler Hintergrund
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.surface.blit(overlay, (0, 0))

        # roter Rahmen
        pygame.draw.rect(
            screen.surface,
            (150, 0, 0),
            Rect((WIDTH//2 - 300, HEIGHT//2 - 150), (600, 300))
        )

        pygame.draw.rect(
            screen.surface,
            (255, 255, 255),
            Rect((WIDTH//2 - 300, HEIGHT//2 - 150), (600, 300)),
            5
        )

        screen.draw.text(
            "GAME OVER",
            center=(WIDTH//2, HEIGHT//2 - 50),
            fontsize=40,
            fontname="pixel",
            color="red",
            owidth=2,
            ocolor="white"
        )

        screen.draw.text(
            f"Erreichte Ebene: {current_layer}",
            center=(WIDTH//2, HEIGHT//2 + 20),
            fontsize=30,
            fontname="pixel",
            color="white"
        )

        screen.draw.text(
            "ESC - Neustart",
            center=(WIDTH//2, HEIGHT//2 + 90),
            fontsize=30,
            fontname="pixel",
            color="white"
        )
    if victory_screen:

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.surface.blit(overlay, (0, 0))

        pygame.draw.rect(
            screen.surface,
            (20, 120, 20),
            Rect((WIDTH//2 - 350, HEIGHT//2 - 175), (700, 350))
        )

        pygame.draw.rect(
            screen.surface,
            (255, 255, 255),
            Rect((WIDTH//2 - 350, HEIGHT//2 - 175), (700, 350)),
            5
        )

        screen.draw.text(
            "GEWONNEN!",
            center=(WIDTH//2, HEIGHT//2 - 90),
            fontsize=50,
            fontname="pixel",
            color=(255, 215, 0),
            owidth=2,
            ocolor="black"
        )

        screen.draw.text(
            "Du konntest den Wald befreien!",
            center=(WIDTH//2, HEIGHT//2 - 10),
            fontsize=20,
            fontname="pixel",
            color="white"
        )


        screen.draw.text(
            "ESC - Neues Abenteuer starten",
            center=(WIDTH//2, HEIGHT//2 + 120),
            fontsize=20,
            fontname="pixel",
            color="white"
        )


map1()
def update():
    global map_on , mapdeviationx, current_layer , tree_alive, leafs, angle
    global FRAME_INDEX_WALK, WALK_ANIMATION,SPEED, FRAME_INDEX_IDLE, IDLE_ANIMATION, vy, GRAVITY, MAX_FALL_SPEED, JUMP_SPEED, DIRECTION, CAMERA_X, CAMERA_Y, ATTACKCOOLDOWN_SANDWORMS, map_on
    global reward_screen, victory_screen

    global game_over

    global shop_open, gold

    if victory_screen:
        if keyboard.escape:
            os.execl(sys.executable, sys.executable, *sys.argv)
        return

    if shop_open:

        if keyboard.K_1 and gold >= 30:
            gold -= 30
            mc.regeneration += 1
            time.sleep(0.1)

        if keyboard.K_2 and gold >= 10:
            gold -= 10
            mc.hp += 30
            if mc.hp > 100:
                mc.hp = 100
            time.sleep(0.1)

        if keyboard.K_3 and gold >= 10:
            gold -= 10
            mc.damage_bonus += 0.5
            time.sleep(0.1)

        if keyboard.escape:
            shop_open = False
            map1()

        return

    if mc.hp <= 0:
        game_over = True
    if reward_screen:
        if keyboard.escape:
            reward_screen = False
            map1()
        return
    if game_over:
        if keyboard.escape:
            os.execl(sys.executable, sys.executable, *sys.argv)
        return
    #walking
    mc.stand = True
    
    vx = 0
    
    if keyboard.a:
        vx = -MOVESPEED
        mc.stand = False
        DIRECTION = -1
        
    elif keyboard.d:
        vx = +MOVESPEED
        mc.stand = False
        DIRECTION = 1
    
    #moving mc
    if mc.x + vx > 60 and mc.x + vx  < 2740:
        mc.x += vx
    
    #jumping
    if mc.on_g == True and keyboard.space == True:
        vy = -JUMP_SPEED
    vy = min(vy + GRAVITY, MAX_FALL_SPEED)
    
    if vy > 0:
        
        # Zielposition des Charakters (in der Luft)
        target = mc.bottom + vy
        
        # niedrigst mögliche Landeposition (Boden oder Plattform)
        landing_bottom = 623
        
        
        # Plattformkollisionen überprüfen
        for platform in platform_draw:

            above = (mc.right - 85 > platform.left and mc.left + 93 < platform.right)

            # Spieler war vorher unter der Plattform
            falling_onto_platform = (mc.bottom <= platform.top + 70 and target >= platform.top+70)

            if above and falling_onto_platform:
                landing_bottom = platform.top +70
                break


        #checken ob durch den boden fallen würde
        if target >= landing_bottom:
            mc.bottom = landing_bottom
            vy = 0 
            mc.on_g = True
        
        else:
            mc.y = mc.y + vy
            mc.on_g = False
    
    # y-Bewegung nach oben ausführen
    else:
        mc.y += vy
        mc.on_g = False
    CAMERA_X = mc.x - 704
    CAMERA_Y = mc.y - 500
    #kamera begrenzen
    CAMERA_X = max(0, CAMERA_X)
    CAMERA_X = min(CAMERA_X, 2816 - WIDTH)

    mc.damage = False

    #gegner attackieren
    for enemy in enemies[:]:
        mc.hitbox = Rect(mc.left + 100, mc.top + 141, mc.width - 100, mc.height - 30)
        enemy.damage = False
        if enemy.hp <= 0:
            enemies.remove(enemy)
        if enemy.type == 'sandwurm':
            if mc.on_g == True: 
                enemy.timer+=1
            #animation
            if enemy.timer == 14 and enemy.state == 'up':
                enemy.state = 'empty'

            if enemy.timer == ATTACKCOOLDOWN_SANDWORMS-14 and enemy.state == 'empty':
                enemy.state = 'down'

           # attack
            if enemy.timer >= ATTACKCOOLDOWN_SANDWORMS and mc.on_g == True:
                enemy.pos = (mc.x, mc.y + 83)
                enemy.state = 'up'
                enemy.timer = 0
            enemy.hitbox = Rect(enemy.left + 20,enemy.top + 50,enemy.width - 40,enemy.height)
            if enemy.hitbox.colliderect(mc.hitbox) and enemy.timer >= 20 and mc.damage == False:
                mc.hp -= 0.5
                mc.damage = True

        if enemy.type == 'fly':
            center = Vector2(1200, 270)
            enemy.timer += 1

            distance_to_player = Vector2(enemy.pos).distance_to(mc.pos)
            #fly movement
            if distance_to_player < 500:
                # vor dem Spieler fliehen
                direction = Vector2(enemy.pos) - Vector2(mc.pos)

                if direction.length() != 0:
                    direction = direction.normalize()

                enemy.x += direction.x * enemy.speed*0.7
                enemy.y=min(enemy.y + direction.y * enemy.speed*0.8, 623) 

            else:
                # Kreisflug
                enemy.angle += 0.005

                target = Vector2(center.x + 2000 * math.cos(enemy.angle),center.y + 500 * math.sin(enemy.angle))

                direction = target - Vector2(enemy.pos)

                if direction.length() > 0:
                    direction = direction.normalize()
                    enemy.x += direction.x * enemy.speed*0.5
                    enemy.y = min(enemy.y + direction.y * enemy.speed*0.5, 630)

            if enemy.timer >= 300:
                enemy.timer = 0
                enemy_shoot(enemy.pos)
            if direction.x > 0:
                enemy.direction = 1
            else:
                enemy.direction = -1
    
    for leaf in leafs:
        mc.hitbox = Rect(mc.left + 100, mc.top + 141, mc.width - 200, mc.height - 30)
        leaf.angle += 0.01
        angle += 0.0005
        leaf.pos = ((1500+400*math.sin(angle)) +800 * math.cos(leaf.angle),350 +150* math.sin(leaf.angle))
        if leaf.colliderect(mc.hitbox):
            mc.hp -= 0.5
            mc.damage = True
    #bullet travel
    for bullet in bullets:
            bullet.x += bullet.velocity.x
            bullet.y += bullet.velocity.y
            #abstand zur zielposition prüfen
            distance = Vector2(bullet.pos).distance_to(bullet.target)
            if distance < BULLET_SPEED:
                #explosion erstellen
                explotion = Actor('explosion0.png')
                explotion.pos = bullet.pos
                explotions.append(explotion)
                explotion.timer = 3
                explotion.count = 0
                #bullet entfernen
                bullets.remove(bullet)
    #neues level
    if not enemies and not map_on and not reward_screen:
        level_complete()
    if tree_alive == True:
        if enemies[0].type != 'tree':
            tree_alive = False
            mc.regeneration += 0.5
            mc.damage_bonus += 0.5

        if len(enemies) == 1 :
            sandwurm(random.randint(max(2,current_layer-7),max(1,current_layer*2)))
            fly(random.randint(max(2,current_layer-7),max(0,current_layer*2)))
    global boss_alive
    if boss_alive == True:
        if enemies[0].hp < 500:
            enemies[0].image = 'boss2.png'
            if leafs == []:
                leaf1(20)
        if enemies[0].type != 'boss':
            boss_alive = False
            leafs= []
            victory_screen = True
        if len(enemies) < 3 :
            fly(random.randint(4,12))
    #enemy bullets
    for bullet in enemy_bullets[:]:
        bullet.x += bullet.velocity.x
        bullet.y += bullet.velocity.y
        if bullet.y > bg.bottom or bullet.y < bg.top or bullet.x < bg.left or bullet.x > bg.right:
            enemy_bullets.remove(bullet)

    #animation walking
    if mc.stand == False and mc.on_g == True :
        FRAME_INDEX_IDLE = 0
        WALK_ANIMATION -= 1
        
        #fliping through images
        if WALK_ANIMATION == 0 and DIRECTION == 1:  
            WALK_ANIMATION = SPEED
            mc.image = walk_frames[FRAME_INDEX_WALK]
            FRAME_INDEX_WALK = (FRAME_INDEX_WALK + 1) % 4
        elif WALK_ANIMATION == 0 and DIRECTION == -1:  
            WALK_ANIMATION = SPEED
            mc.image = walk_frames[FRAME_INDEX_WALK+4]
            FRAME_INDEX_WALK = (FRAME_INDEX_WALK + 1) % 4

    #animation idle
    if mc.on_g == True and mc.stand == True and DIRECTION == 1:
        FRAME_INDEX_WALK = 0
        IDLE_ANIMATION -= 1
        #fliping through images
        if IDLE_ANIMATION == 0:  
            IDLE_ANIMATION = SPEED+2
            mc.image = idle_frames[FRAME_INDEX_IDLE]
            FRAME_INDEX_IDLE = (FRAME_INDEX_IDLE + 1) % 5
    elif mc.on_g == True and mc.stand == True and DIRECTION == -1:
        FRAME_INDEX_WALK = 0
        IDLE_ANIMATION -= 1
        #fliping through images
        if IDLE_ANIMATION == 0:  
            IDLE_ANIMATION = SPEED+2
            mc.image = idle_frames[FRAME_INDEX_IDLE+5]
            FRAME_INDEX_IDLE = (FRAME_INDEX_IDLE + 1) % 5
    #animation springen
    if mc.on_g == False and DIRECTION == 1:
        mc.image = 'mage_jump1'
    elif mc.on_g == False and DIRECTION == -1:
        mc.image = 'mage_jump_reverse'
    #animation firebullet
    for bullet in bullets:
        bullet.frame_index = (bullet.frame_index + 1) % 3
        bullet.image = fire_ball_frames[bullet.frame_index]
        for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    enemy.hp -= 1 + mc.damage_bonus
                    enemy.damage = True
    
    #damage enemybullets
    for bullet in enemy_bullets[:]:
        mc.hitbox = Rect(mc.left + 100, mc.top + 141, mc.width - 200, mc.height - 30)
        bullet.hitbox = Rect(bullet.left+10, bullet.top+10, bullet.width-10, bullet.height-10)
        if bullet.image == 'enemy_bullet.png':
            if bullet.hitbox.colliderect(mc.hitbox):
                mc.hp -= 5
                mc.damage = True
                enemy_bullets.remove(bullet)

    for explotion in explotions:
        explotion.count = (explotion.count + 1) % 2
        if explotion.count == 0:
            explotion.image = explotion_frames[(4-explotion.timer)]
            explotion.timer -= 1
            if explotion.timer < 0:
                explotions.remove(explotion)
        for enemy in enemies[:]:

                if explotion.colliderect(enemy):
                    enemy.hp -= 1 + mc.damage_bonus
                    enemy.damage = True
    
    #animation sandwurm               
    for enemy in enemies[:]:
        if enemy.type == 'sandwurm':
            if mc.on_g == True:
                enemy.animationdelay = (enemy.animationdelay + 1)%2
                if enemy.state == 'up' and enemy.animationdelay == 0:
                    enemy.image = sandwurm_frames[enemy.frame_index]
                    enemy.frame_index = (enemy.frame_index + 1) % 7
                elif enemy.state == 'down' and enemy.animationdelay == 0:
                    enemy.image = sandwurm_frames[enemy.frame_index+6]
                    enemy.frame_index = (enemy.frame_index + 1) % 7
                elif enemy.damage == False and enemy.state == 'empty':
                    enemy.image = 'sandwurm_up6.png'
            if enemy.damage == True:
                enemy.image = 'sanwurm_damage.png'
        if enemy.type =='fly':
            if enemy.direction == 1:
                enemy.image = fly_frames[round((enemy.timer%32)/8)+5]
            if enemy.direction == -1:
                enemy.image = fly_frames[round((enemy.timer%32)/8)]
            

    if not map_on:
        map.x = -3000
        mapdeviationx = -3000

    global mapdeviation
    if keyboard.w:
        map.y += 10
        mapdeviation += 10  
    if keyboard.s and map.bottom -10 > HEIGHT:
        map.y -= 10
        mapdeviation -= 10 


    if mc.hp < mc.max_hp:
        mc.hp = min(mc.max_hp, mc.hp + mc.regeneration * 0.04)           
                

            

            
pgzrun.go()