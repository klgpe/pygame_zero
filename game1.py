import pgzrun
import random
import pygame
import math
from pygame import Rect
from pygame.math import Vector2

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
special_locations = random.sample(range(1,14), 5)
location_shops = special_locations[:3]
location_elites = special_locations[3:]

start = random.randint(0, columns-1)

for row in range(rows):
    path_information.append((start,row))
    start = random.randint(start-1, start +1)
    if start>4:
        start = 4
    if start<0:
        start = 0

for i in range(rows):
    path.append((positions[path_information[i][0]],positions[path_information[i][1]+5]))
path.append((700,250))
map = Actor('map.png')

for positions in path:
    if path.index(positions) in location_shops:
        location = Actor('shop.png')
        location.type = 'shop'
        location.layer = path.index(positions)
    elif path.index(positions) in location_elites:
        location = Actor('elite.png')
        location.type = 'elite'
        location.layer = path.index(positions)
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




#platformen in Listen
platforms = [Actor("platform0"),Actor("platform1"),Actor("platform2"),Actor("platform3"),Actor("platform0"),Actor("platform1"),Actor("platform2"),Actor("platform3")]
platform_pos_topleft = [(700,270),(900, -50), (1550,200),( 1900, 50),(300,220),(500, -10), (1500, -100),(1100, 300),(2000,220)]
platform_draw = []

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


#fire_bullet
bullets = []
explotions =[]

mc.stand = True
mc.on_g = True

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

def launch(type):
    
    global platform_draw, enemies, current_layer
    if type == 'enemy':
        #lsite mit echten platformen erstelen
        platform_draw = []
        platform_draw = platformlist(platforminformation())
        #startposition der platformen merken
        #sandwürmer spawnen
        current_layer += 1
        sandwurm(random.randint(max(2,current_layer-7),max(1,current_layer+2)))
        fly(random.randint(max(2,current_layer-7),max(0,current_layer+4)))
    
    
    

def fly(anzahl):
    for i in range(anzahl):
        fly = Actor('fly_left0')
        fly.type = 'fly'
        fly.pos = 1500,500
        fly.hp = 10
        fly.speed =4
        fly.direction = 1
        fly.timer = random.randint(0,500) #timer
        fly.angle = random.uniform(0,360)
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
    global map_on
    if map_on == True:
        for positions in drawn_positions:
            hitbox = Rect(positions.left, positions.top -3200 +250*max(0,current_layer)+mapdeviation, positions.width, positions.height)
            
            if hitbox.collidepoint(pos):
                print("geklickt:", positions.type, positions.layer)
                if positions.type == 'shop'and positions.layer == current_layer:
                    launch('shop')
                elif positions.type == 'elite'and positions.layer == current_layer :
                    launch('elite')
                elif positions.type == 'enemy'and positions.layer == current_layer:
                    launch('enemy')
                elif positions.type == 'boss' and positions.layer == current_layer:
                    launch('boss')
                map_on = False
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
    map.bottom = HEIGHT +250*max(0,current_layer)
    map.x = WIDTH/2
    map_on = True

#kamera funktion
def camera(pos):
    x, y = pos
    return (x - CAMERA_X, y - CAMERA_Y)

def draw():
    global map_on , mapdeviationx, current_layer 
 # Hintergrund
    screen.blit(bg.image,(bg.left - CAMERA_X * 0.5, bg.top - CAMERA_Y * 0.5))

    # Boden
    screen.blit(ground.image,camera(ground.topleft))

    # Plattformen
    for platform in platform_draw:
        screen.blit(platform.image,camera(platform.topleft))

    # Bullets
    for bullet in bullets:
        screen.blit(bullet.image,camera(bullet.topleft))

    # Spieler
    screen.blit(mc.image, camera(mc.topleft))  

    #gegner
    for enemy in enemies:
        screen.blit(enemy.image, camera(enemy.topleft))
    
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
    
    map.draw()
    for i in range(current_layer):
        pygame.draw.line(screen.surface, "black",
                     (path[i][0]+mapdeviationx,path[i][1]-3200+250*max(0,current_layer)+mapdeviation), (path[i + 1][0]+mapdeviationx,path[i + 1][1]-3200+250*max(0,current_layer)+mapdeviation), 5)
    for position in drawn_positions:
        screen.blit(position.image,( position.left+mapdeviationx , position.top -3200 +250 * max(0,current_layer)+mapdeviation))
map1()
def update():
    global map_on , mapdeviationx, current_layer 
    global FRAME_INDEX_WALK, WALK_ANIMATION,SPEED, FRAME_INDEX_IDLE, IDLE_ANIMATION, vy, GRAVITY, MAX_FALL_SPEED, JUMP_SPEED, DIRECTION, CAMERA_X, CAMERA_Y, ATTACKCOOLDOWN_SANDWORMS, map_on
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
                mc.hp -= 1
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
    if not enemies:
        map1()

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
                    enemy.hp -= 1
                    enemy.damage = True
    
    #damage enemybullets
    for bullet in enemy_bullets[:]:
        mc.hitbox = Rect(mc.left + 100, mc.top + 141, mc.width - 200, mc.height - 30)
        bullet.hitbox = Rect(bullet.left+10, bullet.top+10, bullet.width-10, bullet.height-10)
        if bullet.image == 'enemy_bullet.png':
            if bullet.hitbox.colliderect(mc.hitbox):
                mc.hp -= 2
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
                    enemy.hp -= 1
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
    if keyboard.s:
        map.y -= 10
        mapdeviation -= 10 
                
                

            

            
pgzrun.go()