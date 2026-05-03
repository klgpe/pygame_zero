import pgzrun

WIDTH = 1398
HEIGHT = 766
MOVESPEED = 9
JUMP_SPEED = 22
GRAVITY = 0.8
MAX_FALL_SPEED = 30
vx = 0
vy = 0

platforms= []

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



def draw():
    # Zeichne Hintergrund
    bg.draw()
    #character malen
    mc.draw()
    #zeichne untergrund
    ground.draw()
    

    

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
    
    #moving mc
    elif mc.x - vx > 0 and mc.x - vx  < 1390:
        mc.x -= vx
    
    #jumping
    if mc.on_g == True and keyboard.space == True:
        vy = -JUMP_SPEED
    vy = min(vy + GRAVITY, MAX_FALL_SPEED)
    
    if vy >= 0:
        
        # Zielposition des Charakters (in der Luft)
        target = ground.top - vy
        
        # niedrigst mögliche Landeposition (Boden oder Plattform)
        landing_bottom = 0
        
        # Plattformkollisionen überprüfen
        for platform in platforms:
            if (mc.right -85 > platform.left and mc.left + 93 < platform.right and mc.bottom -10  <= platform.top):
                landing_bottom = min(landing_bottom, platform.top)

        if target <= landing_bottom:
            ground.top = 0
            bg.top = -300
            vy = 0 
            mc.on_g = True
        else:
            ground.top = target
            bg.top = bg.top -vy/2
            mc.on_g = False
    # y-Bewegung nach oben ausführen
    else:
        bg.top -= vy/2
        ground.top -= vy
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