
import pygame, sys, os
from PIL import Image, ImageOps
import numpy
from pygame import *
import math
import _thread
WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

IMAGE_SIZES = {}
IMAGES = {}
PATH="Resources/"


class Level():
    def __init__(self, level, player_settings, bg_music):
        self.screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
        self.bg = pygame.Surface((32,32))
        self.bg.convert()
        self.entities = pygame.sprite.Group()

        self.platforms = []
        self.decorations = []
        self.enemies = []
        x = y = 0
        self.level = level
        # build the level
        for row in level:
            for col in row:
                if col == "1":
                    p = Platform(x, y, "platform/jungle_pack_07.png")
                    self.platforms.append(p)
                    self.entities.add(p)

                if col == "2":
                    p = Platform(x, y, "platform/jungle_pack_35.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "P":
                    p = Platform(x, y, "platform/jungle_pack_05.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "3":
                    p = Platform(x, y, "platform/jungle_pack_03.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "4":
                    p = Platform(x, y, "platform/jungle_pack_11.png")
                    self.platforms.append(p)
                    self.entities.add(p)

                if col == "5":
                    p = Platform(x, y, "platform/jungle_pack_19.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "6":
                    p = Platform(x, y, "platform/jungle_pack_21.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "7":
                    p = Platform(x, y, "platform/jungle_pack_40.png")
                    self.platforms.append(p)
                    self.entities.add(p)
                if col == "E":
                    e = ExitBlock(x, y)
                    self.platforms.append(e)
                    self.entities.add(e)
                if col == "Q":
                    q = EnemyMosquito(x, y)
                    self.enemies.append(q)
                    self.entities.add(q)
                if col == "S":
                    s = EnemySpider(x, y)
                    self.enemies.append(s)
                    self.entities.add(s)

                if col == "0":
                    p = Platform(x, y, "platform/jungle_pack_09.png")
                    self.platforms.append(p)
                    self.entities.add(p)

                if col == "D":
                    d = Decoration(x, y, 128,128, "platform/jungle_pack_67.png")
                    self.decorations.append(d)
                    self.entities.add(d)

                if col == "!":
                    d = Decoration(x, y, 128,128, "platform/jungle_pack_59.png")
                    self.decorations.append(d)
                    self.entities.add(d)

                if col == "¡":
                    d = Decoration(x, y, 128,128, "platform/jungle_pack_57.png")
                    self.decorations.append(d)
                    self.entities.add(d)
                if col == "B":
                    d = Decoration(x, y, 128,128, "platform/jungle_pack_66.png")
                    self.decorations.append(d)
                    self.entities.add(d)

                #player
                if col == "F":
                    self.player = Player(x, y, player_settings[2])
                x += 32
            y += 32
            x = 0
        self.total_level_width  = len(level[0])*32
        self.total_level_height = len(level)*32

        self.camera = Camera(Camera.complex_camera, self.total_level_width, self.total_level_height)
        self.entities.add(self.player)
        self.backGround = Background(PATH+'platform/bg_jungle.png', [0,0], (1280, 720))

        self.playmusic(bg_music)
    def update(self, up, down, left, right, space, running):
        # draw background
        for y in range(32):
            for x in range(32):
                self.screen.blit(self.bg, (x * 32, y * 32))

        self.camera.update(self.player)
        self.screen.fill([255, 255, 255])
        self.screen.blit(self.backGround.image, self.backGround.rect)
        # update player, draw everything else
        if not self.player.update(up, down, left, right, space, running, self.platforms, self.enemies, self.total_level_height):
            return False
        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))
    def playmusic(self, file):
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(-1, 0.0)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, screen_sizes):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (1280, 720))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Media_Screen():
    def __init__(self, timer, bg):
        self.timer = timer
        #self.bg=bg
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.timer.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self,text,size,color,x,y):
        font = pygame.font.Font('freesansbold.ttf',size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

class Start_Screen(Media_Screen):
    def __init__(self, timer):
        Media_Screen.__init__(self, timer,(Background(PATH+'platform/bg_jungle.png', [0,0], (1280, 720))))
        self.screen=pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.show_start_screen()
    def show_start_screen(self):
        # game splash/start screen
        image = pygame.image.load(PATH+"logo.png")
        image = pygame.transform.scale(image,(550,200))
        image_width, image_height= image.get_size()
        self.screen.blit(image,((WIN_WIDTH-image_width)/2,(WIN_HEIGHT-image_height)/3))
        self.draw_text("PRESS ANY KEY",32,(240,248,255),WIN_WIDTH/2,WIN_HEIGHT*3 /4)
        pygame.display.flip()
        self.running = True
        self.wait_for_key()
        if not self.running:
            pygame.quit()
            sys.exit()
def main():
    global cameraX, cameraY
    pygame.init()

    pygame.display.set_caption("Froggy!")
    timer = pygame.time.Clock()

    screen=Start_Screen(timer)

    up = down = left = right = space = running = False
    #para cambiar niveles cambiar el nombre a level (no duplicados)

    level1 = [
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                             Q                               ",
        "                                                                                                               3PPP1         ",
        "                                                                                                               22222         ",
        "                                                                                              D                22222         ",
        "                                                                                           3PPPPPPP1           22222         ",
        "                                                                                           222222222           22222PPPPPPPPP",
        "                                                                                           222222222           22222222222222",
        "                                                                                      B    222222222           22222222222222",
        "                                                                              S    3PPPPPPP222222222           22222222222222",
        "                                                                          3PPPPPPPP22222222222222222           22222222222222",
        "                                                                      !   22222222222222222222222222           22222222222222",
        "                                                   B                 3PPPP22222222222222222222222222           22222222222222",
        "                                                5PPPPPP7          0PP2222222222222222222222222222222           22222222222222",
        "                                        B        666666             66662222222222222222222222222222           22222222222222",
        "                                      PPPPPP                            6666222222222222222222222222           22222222222222",
        "                                      622226                                662222222222222222222222           22222222222222",
        "                                       6666                                   6666666666666222222222           22222222222222",
        "                                                                                           222222222           22222222222222",
        "    ¡  F     !                   B          D     ¡                     D                  222222222           22222222222222",
        "PPPPPPPPPPPPPPPPPP1         3PPPPPPPPPPPPPPPPPPPPPPPP1         P     3PPPPPPPPPPPPPPPPPPPP2222222222           22222222222222"]

    level= [
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                            B                                  B                                             ",
        "                               3PPPPPPPPPPPPPPPPPPPP1                 3PPPPPPPPPPPPPPPPPPPP1                                 ",
        "                               6666666222222222222222                 2222222222222222666666                                 ",
        "                      PPP             666666666666666                 6666666666666666            PPP                        ",
        "                      666                                                                         666                        ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                 PPP                                                                                  PPP                    ",
        "                 666                                                                                  666                    ",
        "  F!                                 B                        B                  D                                   ¡       ",
        "PPPPPPPPPPPP1                  3PPPPPPPPPPP1        3PPPPPPPPPPPPPPPPP1        3PPPPPPPPPPP1                    3PPPPPPPPPPPP",
        "2222222266666                  6666662222222        2222222222222222222        2222222266666                    6666622222222",
        "22226666                             6666666        6666666666666666666        66666666                              22222222",
        "6666                                                                                                                 22222222",
        "                                                                                                                     22222222",
        "              PPP                                                                                         PPP        22222222",
        "              666                                                                                         666        22222222",
        "                                                                                                                     22222222",
        "                                                                                                                     22222222",
        "                          B                                                                   B                      22222222",
        "                       3PPPPP1                  B                                            3PPPPP1                 22222222",
        "                       6666662PPPPPPP1      3PPPPPP1        3PPP1      3PPPPPP1        PPPPPP2666666                 22222222"]



    level3 = [
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             "]




    level_vacio = [
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             ",
        "                                                                                                                             "]



    player_settings = (32, 32,PATH+ "froggy.png")

    
    level = Level(level, player_settings, PATH+'bg_music1.ogg')


    done = play_again = False
    while not (done or play_again):
        timer.tick(60)


        for e in pygame.event.get():
            if e.type == QUIT:
                done = True
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                paused = True#change for paused menu
                pause()
                up = down = left = right = space = running = False
                pygame.event.clear()
                break
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                space = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_SPACE:
                space = False
        if(level.update(up, down, left, right, space, running)==False):
            play_again = True
        pygame.display.update()
    if(play_again):
        main()
    else:
        pygame.quit()
def pause():
    pygame.event.clear()
    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                return
class Camera(object):

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    def simple_camera(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

    def complex_camera(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
        t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class EnemyMosquito(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 4.0
        self.yvel = 4.0
        self.follow = False
        self.onGround = False
        self._image_origin = pygame.image.load(PATH + "mosquito1.png")
        self._image_origin = pygame.transform.scale(self._image_origin, (32, 32)).convert_alpha()
        self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
        self.image  = self._image_origin
        image_rect = (self.image.get_rect().size)
        self.image.convert()
        self.rect = Rect(x, y, image_rect[0], image_rect[1])
    def update(self, platforms, posX, posY):
        self.xvel = 4.0
        self.yvel = 4.0
        self.move_towards_player(posX, posY)
        self.collide(self.xvel, 0, platforms)
        self.collide(0, self.yvel, platforms)

    def move_towards_player(self, posX, posY):
        # find normalized direction vector (dx, dy) between enemy and player
        dx, dy = self.rect.x - posX, self.rect.y - posY
        dist = math.hypot(dx, dy) #math.sqrt(dx*dx + dy*dy)
        if not self.follow:
            if dist < 400:
                self.follow = True
            else:
                return
        try:
            dx, dy =  dx*-1.0 / dist, dy*-1.0 / dist
        except ZeroDivisionError:
            print("Divided by zero")
        # move along this normalized vector towards the player at current speed
        self.xvel, self.yvel = dx * self.xvel, dy * self.yvel
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if dx > 0:
            self.image = self._image_toLeft
        else:
            self.image = self._image_origin
    def observar(self, posX, posY, platforms):
        self.update(platforms, posX, posY)
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if abs(self.rect.right - p.rect.left) < 5:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                    print ("Enemy collide right")
                if abs(self.rect.left - p.rect.right) < 5:
                    self.rect.left = p.rect.right
                    self.xvel = 0
                    print ("Enemy collide left")
                if abs(self.rect.bottom - p.rect.top) < 5:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                if abs(self.rect.top - p.rect.bottom) < 5:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    print ("Enemy collide top")

class EnemySpider(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 4.0
        self.yvel = 4.0
        self.follow = False
        self.onGround = False
        self._image_origin = pygame.image.load(PATH + "spider1.png")
        self._image_origin = pygame.transform.scale(self._image_origin, (32, 32)).convert_alpha()
        self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
        self.image  = self._image_origin
        image_rect = (self.image.get_rect().size)
        self.image.convert()
        self.rect = Rect(x, y, image_rect[0], image_rect[1])
    def update(self, platforms, posX, posY):
        self.xvel = 6.0
        self.yvel = 4.0
        self.move_towards_player(posX, posY)
        self.collide(self.xvel, 0, platforms)
        self.collide(0, self.yvel, platforms)

    def move_towards_player(self, posX, posY):
        dist = math.hypot(self.rect.x - posX, self.rect.y - posY) #math.sqrt(dx*dx + dy*dy)
        if not self.follow:
            if dist < 200:
                self.follow = True
            else:
                return
        dx = posX - self.rect.x
        self.rect.y += 4.0
        if dx > 0:
            self.image = self._image_toLeft
            self.rect.x +=self.xvel
        elif dx < 0:
            self.image = self._image_origin
            self.rect.x -=self.xvel

    def observar(self, posX, posY, platforms):
        self.update(platforms, posX, posY)
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if abs(self.rect.right - p.rect.left) < 5:
                    self.rect.right = p.rect.left
                    self.xvel = 0
                    print ("Enemy collide right")
                if abs(self.rect.left - p.rect.right) < 5:
                    self.rect.left = p.rect.right
                    self.xvel = 0
                    print ("Enemy collide left")
                if abs(self.rect.bottom - p.rect.top) < 5:
                    self.rect.bottom = p.rect.top
                    self.yvel = 0
                if abs(self.rect.top - p.rect.bottom) < 5:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    print ("Enemy collide top")

class Player(Entity):
    def __init__(self, x, y, image_path):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        
        self._image_origin = pygame.image.load(PATH +"sprite_froggy0.png")
        self._image_origin = pygame.transform.scale(self._image_origin, (52, 52)).convert_alpha()
        self._image_toLeft = pygame.transform.flip(self._image_origin, True, False).convert_alpha()
        self.image  = self._image_origin
        
        image_rect = (self.image.get_rect().size)
        self.rect = Rect(x, y, image_rect[0], image_rect[1])
        self.tongue = 0

        #todas las demas imagenes
        path_tongue = "froggy_tongue/"


        self.imagenes_derecha = []
        self.imagenes_izquierda = []
        self.imagenes_derecha.append(self._image_origin)
        self.imagenes_izquierda.append(self._image_toLeft)
        for i in range(3):
            i=i+1
            im = pygame.image.load(PATH+ path_tongue+"froggy_tongue_"+str(i)+".gif")
            im = pygame.transform.scale(im, (52, 52)).convert_alpha()
            self.imagenes_derecha.append(im)
            im_toLeft = pygame.transform.flip(im, True, False).convert_alpha()
            self.imagenes_izquierda.append(im_toLeft)

        
        self.lado = 'derecha'
        self.animacion = Animacion()
        

        ################
        self.forma = [0, 'ida']
        self.sacandolengua=False
    def update(self, up, down, left, right, space, running, platforms, enemies, level_high):
        vida = True
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        #if running:
            #self.xvel = 12
        if left:
            self.xvel = -8
            self.lado = 'izquierda'
        if right:
            self.xvel = 8
            self.lado = 'derecha'
        if space:
            if self.tongue <= 0:
                self.tongue = 100
        #print(self.tongue)

        
        if space and self.sacandolengua==False:
            try:
                _thread.start_new_thread(self.sacarlengua, ())
            except Exception:
                print("Error en hilo")
        #cambiar imagen
        if self.lado == 'izquierda':
            self.image = self.imagenes_izquierda[self.forma[0]]
        else:
            self.image = self.imagenes_derecha[self.forma[0]]
        
                
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        if (self.tongue>=0):
            self.tongue-=1
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)
        vida = self.collide_enemies(enemies)
        self.beobserver(enemies, platforms)
        
        if(self.rect.y>level_high or (vida)):
            return False
        else:
            return True
    def sacarlengua(self):
        self.sacandolengua=True
        dt = pygame.time.Clock()
        for i in range(6):
            dt.tick(5)
            self.forma = self.animacion.animarCompleta(self.imagenes_derecha, self.forma)
        self.sacandolengua=False

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                    print ("collide right")
                if xvel < 0:
                    self.rect.left = p.rect.right
                    print ("collide left")
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
                    print ("collide top")

    def collide_enemies(self, enemies):
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                print("--------CHOCA------")
                return True
        return False
    def beobserver(self, enemies, platforms):
        for q in enemies:
            #if isinstance(q, Enemy):
            q.observar(self.rect.x, self.rect.y, platforms)


def crop(image_name, rx, ry):
        pil_image = Image.open(image_name)
        size = (pil_image.width, pil_image.height)
        np_array = numpy.array(pil_image)
        blank_px = [255, 255, 255, 0]
        mask = np_array != blank_px
        coords = numpy.argwhere(mask)
        try:
            x0, y0, z0 = coords.min(axis=0)
            x1, y1, z1 = coords.max(axis=0) + 1
            cropped_box = np_array[x0:x1, y0:y1, z0:z1]
            pil_image = Image.fromarray(cropped_box, 'RGBA')
        except Exception:
            pass
        print(image_name + str((pil_image.width, pil_image.height)))
        return (pil_image.width*rx/size[0], pil_image.height*ry/size[1])


class Platform(Entity):
    def __init__(self, x, y, image_path):
        Entity.__init__(self)

        image_rect = None
        try:
             image_rect = IMAGE_SIZES[PATH + image_path]
             self.image = IMAGES[(PATH + image_path, 32, 32)]
        except KeyError:
            image_rect = crop(PATH + image_path, 32, 32)
            IMAGE_SIZES[PATH + image_path] = image_rect
            if (PATH + image_path,32,32) not in IMAGES:
                self.image = pygame.image.load(PATH + image_path)
                self.image = pygame.transform.scale(self.image, (32, 32)).convert_alpha()
                IMAGES[(PATH + image_path,32,32)] = self.image
        self.rect = Rect(x, y, image_rect[0], image_rect[1])
    def update(self):
        pass

class Decoration(Entity):
    def __init__(self, x, y, w, h, image_path):
        Entity.__init__(self)

        self._image_origin = pygame.image.load(PATH + image_path)
        self._image_origin = pygame.transform.scale(self._image_origin, (w, h))
        self.image  = self._image_origin

        image_rect = None
        try:
             image_rect = IMAGE_SIZES[PATH + image_path]
        except KeyError:
            image_rect = crop(PATH + image_path, w, h)
            IMAGE_SIZES[PATH + image_path] = image_rect
        self.rect = Rect(x, y-h+32, image_rect[0], image_rect[1])

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y, "platform/18.png")


class Animacion:
    def __init__(self):
        pass
        
    def animarCompleta(self, imagenes, forma):

        # es +1 ya que en la ultima posicion va a ir si es ida o vuelta
        if forma[0] +1 == len(imagenes):
            forma[1] = 'vuelta'

        # se verifica si esta en la ida o vuelta
        if forma[1] == 'ida':
            forma[0] = forma[0] + 1
            
        elif forma[1] == 'vuelta':
            forma[0] = forma[0] -1

            if forma[0] == 0:
                forma[1] = 'ida'

        
        return forma
    

    def animarIda(self, imagenes, i):

        # es +1 ya que aca no hay ida o vuelta
        if i +1 == len(imagenes):
            i =0

        else:
            i = i+1
        return i

if __name__ == "__main__":
    main()
