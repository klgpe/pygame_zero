import pgzrun
import random

WIDTH = 1398
HEIGHT = 766
MOVESPEED = 9
JUMP_SPEED = 22
GRAVITY = 0.8
MAX_FALL_SPEED = 30
vx = 0
vy = 0

platforms = [Actor("platform0"),Actor("platform1"),Actor("platform2"),Actor("platform3"),Actor("platform0"),Actor("platform1"),Actor("platform2"),Actor("platform3"),
]
platform_pos_topleft = [(700,270),(900, -50), (1550,200),( 1900, 50),(300,220),(500, -10), (1500, -100),(1400, 300),(2000,220)]

walk_frames = ["mage_walk1","mage_walk2",'mage_walk5',"mage_walk4"]
idle_frames = ['mage_idle0','mage_idle1','mage_idle2','mage_idle3','mage_idle4']
FRAME_INDEX_WALK = 0
FRAME_INDEX_IDLE = 0
SPEED = 8
WALK_ANIMATION = SPEED
IDLE_ANIMATION = SPEED +2


#backround
bg = Actor('background.png', topleft=(0,-300))

#untergrund
ground = Actor('untergrund.png', topleft=(0,00))

#character  
mc = Actor('mage.png',midbottom=(704,623))

mc.stand = True
mc.on_g = True

#platformen und orte (indexe) auswählen
def platforminformation():
    return random.sample(range(8), 5 )+ random.sample(range(9), 5)
#platformen und positionen werden anhand von indexen rausgesucht und die platformen dann in eine liste zusammen gefügt
def platformlist(list):
    platform_draw_setup = []
    
    # 4 platformen pro stage
    
    for platform_index in range(5):
        
        #platform desing wird rausgesucht
        actor = platforms[list[platform_index]]
        
        #platformposition wird zugeordnet
        actor.topleft = platform_pos_topleft[list[platform_index + 5]]
        
        #platform wird an liste gefügt 
        platform_draw_setup.append(actor)
    
    return platform_draw_setup 
#lsite mit echten platformen erstelen
platform_draw = []
platform_draw = platformlist(platforminformation())
#startposition der platformen merken
platform_start_y = []
for platform in platform_draw:
    platform_start_y.append(platform.top)


def draw():
    # Zeichne Hintergrund
    bg.draw()
    #character malen
    mc.draw()
    #zeichne untergrund
    ground.draw()
    
    for platform in platform_draw:
        platform.draw() 

    

def update():
    global FRAME_INDEX_WALK, WALK_ANIMATION,SPEED, FRAME_INDEX_IDLE, IDLE_ANIMATION, vy, GRAVITY, MAX_FALL_SPEED, JUMP_SPEED
    #walking
    mc.stand = True
    
    vx = 0
    
    if keyboard.a:
        vx = MOVESPEED
        mc.stand = False
    elif keyboard.d:
        vx = -MOVESPEED
        mc.stand = False
    
    #moving bg
    if ground.x +vx  <= 1408 and ground.x + vx >= -10 and mc.x == 704:
        bg.x += vx / 2
        ground.x += vx
        for platform in platform_draw:
            platform.x += vx
    
    #moving mc
    elif mc.x - vx > 0 and mc.x - vx  < 1390:
        mc.x -= vx
    
    #jumping
    if mc.on_g == True and keyboard.space == True:
        vy = -JUMP_SPEED
    vy = min(vy + GRAVITY, MAX_FALL_SPEED)
    
    if vy > 0:
        
        # Zielposition des Charakters (in der Luft)
        target = ground.top - vy
        
        # niedrigst mögliche Landeposition (Boden oder Plattform)
        landing_bottom = 0
        
        over_platform = False
        # Plattformkollisionen überprüfen
        for platform in platform_draw:
            if mc.right -85 > platform.left and mc.left + 93  < platform.right and mc.bottom - 10 <= platform.top + 60:
                over_platform = True
                #vergleichen ob man durch die platform fallen würden
                differenz_y = min(platform.top - mc.bottom +70 , vy)
                if differenz_y != vy:
                    break
        #wenn durch platform fallen würde, nur auf platform setzten
        if over_platform == True and differenz_y != vy:
            ground.top -= differenz_y
            bg.top -= differenz_y/2
            for platform in platform_draw:
                platform.top -= differenz_y
            mc.on_g = True
            vy = 0
            differenz_y = 0


        #checken ob durch den boden fallen würde
        elif target <= landing_bottom and over_platform == False:
            ground.top = 0
            bg.top = -300
            count = 0
            for platform in platform_draw:
                platform.top = platform_start_y[count]
                count +=1
            vy = 0 
            mc.on_g = True
        
        else:
            ground.top = target
            bg.top = bg.top -vy/2
            for platform in platform_draw:
                platform.top -= vy
            mc.on_g = False
    
    # y-Bewegung nach oben ausführen
    else:
        bg.top -= vy/2
        ground.top -= vy
        for platform in platform_draw:
            platform.top -= vy
        mc.on_g = False

    #animation walking
    if mc.stand == False and mc.on_g == True :
        FRAME_INDEX_IDLE = 0
        WALK_ANIMATION -= 1
        
        #fliping through images
        if WALK_ANIMATION == 0:  
            WALK_ANIMATION = SPEED
            mc.image = walk_frames[FRAME_INDEX_WALK]
            FRAME_INDEX_WALK = (FRAME_INDEX_WALK + 1) % 4

    #animation idle
    if mc.on_g == True and mc.stand == True:
        FRAME_INDEX_WALK = 0
        IDLE_ANIMATION -= 1
        #fliping through images
        if IDLE_ANIMATION == 0:  
            IDLE_ANIMATION = SPEED+2
            mc.image = idle_frames[FRAME_INDEX_IDLE]
            FRAME_INDEX_IDLE = (FRAME_INDEX_IDLE + 1) % 5
    #animation springen
    if mc.on_g == False:
        mc.image = 'mage_jump1'
    
    
pgzrun.go()