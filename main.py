import sys
import pygame
import random
import math

#init pygame
pygame.init()

#init mixerD
pygame.mixer.init()

#init music/sounds
pygame.mixer.music.load('assets/sounds/main_background_music.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

nature_background_music = pygame.mixer.Sound('assets/sounds/nature_background_music.mp3')
nature_background_music.set_volume(0.1)
nature_background_music.play(loops=-1)

basic_jump_sound = pygame.mixer.Sound('assets/sounds/basic_jump.mp3')
basic_jump_sound.set_volume(0.3)

nice_jump_sound = pygame.mixer.Sound('assets/sounds/nice_jump.mp3')
nice_jump_sound.set_volume(0.3)

great_jump_sound = pygame.mixer.Sound('assets/sounds/great_jump.mp3')
great_jump_sound.set_volume(0.3)

perfect_jump_sound = pygame.mixer.Sound('assets/sounds/perfect_jump.mp3')
perfect_jump_sound.set_volume(0.3)

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (127, 127, 127)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


#game loop
game_run = True
pause_run = True
main_menu_run = True

#game window
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 600

#create game window
infoObject = pygame.display.Info()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#game const
SCROLL_THRESHOLD = SCREEN_HEIGHT // 4
GRAVITY = 1
MIN_PLATFORM_H = 110
MAX_PLATFORM_H = 120
MAX_PLATFORM = SCREEN_HEIGHT // MAX_PLATFORM_H + 1
SCALE = 1
HIGH_SCORE = 200
EASY_BORDER = 2000
NORMAL_BORDER = 4000
HARD_BORDER = 6000
HARDCORE_BORDER = 10000


#game variables
end_game = False
scroll = 0
message = ""
score = 0
click = False
time_since_boost = 0
platform = None
platform_list = []
player = None
high_score_y = SCREEN_HEIGHT - HIGH_SCORE

#player const
PLAYER_WIDTH = 44
PLAYER_HEIGHT = 75
PLAYER_ACCELERATION = 2

#platform const
PLATFORM_HEIGHT = 20




pygame.display.set_caption("SkyJump")

bg_image = pygame.image.load("assets/background.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
#platformsd
log = pygame.image.load("assets/platforms/log.png").convert_alpha()
icy = pygame.image.load("assets/platforms/icy.png").convert_alpha()
rock = pygame.image.load("assets/platforms/rock.png").convert_alpha()
sticky = pygame.image.load("assets/platforms/sticky.png").convert_alpha()
grass = pygame.image.load("assets/platforms/grass.png").convert_alpha()

#background
bg_images = []
for i in range(1, 5):
    bg_image = pygame.image.load("assets/background/" "plan_" + str(i) + ".png").convert_alpha()
    # scaled_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_images.append(bg_image)

def draw_bg():
    for bg_image in bg_images:
        screen.blit(bg_image, (0, SCREEN_HEIGHT - 324))



#player class
class Player:
    def __init__(self, x, y):
        self.state = "standing"

        self.idle_image = pygame.image.load("assets/player_sprites/Idle.png").convert_alpha()
        self.idle_image = pygame.transform.scale(self.idle_image, (PLAYER_WIDTH * SCALE, PLAYER_HEIGHT * SCALE))

        self.falling_image = pygame.image.load("assets/player_sprites/Falling.png").convert_alpha()
        self.falling_image = pygame.transform.scale(self.falling_image, (PLAYER_WIDTH * SCALE, PLAYER_HEIGHT * SCALE))

        self.landing_sheet = pygame.image.load('assets/player_sprites/landing_sheet.png').convert_alpha()
        self.landing_frame = 0
        self.LANDING_STEPS = 3
        self.LANDING_ANIMATION_COOLDOWN = 100
        self.landing_last_update = pygame.time.get_ticks()
        self.landing_a_list = self.load_images(self.landing_sheet, self.LANDING_STEPS, SCALE)

        self.walk_sheet = pygame.image.load('assets/player_sprites/walk_sheet.png').convert_alpha()
        self.walk_frame = 0
        self.WALK_STEPS = 7
        self.WALK_ANIMATION_COOLDOWN = 100
        self.walk_last_update = pygame.time.get_ticks()
        self.walk_a_list = self.load_images(self.walk_sheet,self.WALK_STEPS ,SCALE)

        self.jump_sheet = pygame.image.load("assets/player_sprites/jump_sheet.png").convert_alpha()
        self.jump_frame = 0
        self.JUMP_STEPS = 7
        self.JUMP_ANIMATION_COOLDOWN = 100
        self.jump_last_update = pygame.time.get_ticks()
        self.jump_a_list = self.load_images(self.jump_sheet, self.JUMP_STEPS, SCALE)

        self.air_speed = 1
        self.max_speed = 10
        self.acceleration = PLAYER_ACCELERATION
        self.jump_speed = 20

        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH * SCALE, PLAYER_HEIGHT * SCALE)
        self.rect.topleft = (x, y)
        self.max_y = self.rect.bottom
        self.absolute_y = self.rect.bottom

        self.dy = 0
        self.vel_y = 0
        self.dx = 0
        self.vel_x = 0

        self.flip = False
        self.on_ground = True
        self.space_held = True

        self.boost_time = 0
        self.PERFECT_TIME = 1
        self.PERFECT_BOOST = 2
        self.GREAT_TIME = 3
        self.GREAT_BOOST = 1.5
        self.NICE_TIME = 7
        self.NICE_BOOST = 1.25

        self.current_image = self.idle_image




    def get_frame_img(self,frame,sheet,scale,color_key):
        image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
        image.blit(sheet, (0, 0), ((PLAYER_WIDTH * frame), 0, PLAYER_WIDTH, PLAYER_HEIGHT))
        image = pygame.transform.scale(image, (PLAYER_WIDTH * scale, PLAYER_HEIGHT * scale))
        image.set_colorkey(color_key)

        return image

    def load_images(self,sheet, steps,scale):
        a_list = []
        for x in range(steps):
            a_list.append(self.get_frame_img(x,sheet,scale,GRAY))
        return a_list

    def get_image(self, sheet, color_key):
        image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)).convert_alpha()
        image.blit(sheet, (0, 0))
        image.set_colorkey(color_key)
        return image

    def draw(self):
        flipped_current_img = pygame.transform.flip(self.current_image,self.flip,False)
        flipped_current_img.set_colorkey(GRAY)
        screen.blit(flipped_current_img, self.rect)

    def set_img(self,mode):
        if mode == "walking":
            self.current_image = self.walk_a_list[self.walk_frame]
        if mode == "standing":
            self.current_image = self.idle_image
        if mode == "jumping":
            self.current_image = self.jump_a_list[self.jump_frame]
        if mode  == "falling":
            self.current_image = self.falling_image


    def draw_animation(self):
        current_time = pygame.time.get_ticks()
        if self.state == "walking":
            self.set_img("walking")
            if current_time - self.walk_last_update >= self.WALK_ANIMATION_COOLDOWN:
                self.walk_last_update = current_time
                if self.walk_frame == self.WALK_STEPS - 1:
                    self.walk_frame = 0
                else:
                    self.walk_frame += 1

        elif self.state == "jumping":
            self.set_img("jumping")
            if current_time - self.jump_last_update >= self.JUMP_ANIMATION_COOLDOWN:
                self.jump_last_update = current_time
                if self.jump_frame == self.JUMP_STEPS - 1:
                    #stay in that state
                    pass
                else:
                    self.jump_frame += 1

        elif self.state == "landing":
            self.set_img("landing")
            if current_time - self.landing_last_update >= self.LANDING_ANIMATION_COOLDOWN:
                self.landing_last_update = current_time
                if self.landing_frame == self.LANDING_STEPS - 1:
                    #stay in that state
                    pass
                else:
                    self.landing_frame += 1

        elif self.state == "falling":
            self.set_img("falling")

        elif self.state == "standing":
            self.set_img("standing")

    def change_state(self, new_state):
        state = self.state

        if state == "standing":
            self.state = new_state

        elif state == "walking":
            if new_state == "walking":
                pass
            else:
                self.state = new_state
                self.walk_frame = 0

        elif state == "jumping":
            if new_state == "jumping":
                pass
            else:
                self.state = new_state
                self.jump_frame = 0

        elif state == "falling":
            self.state = new_state

        elif state == "landing":
            if new_state == "landing":
                pass
            else:
                self.state = new_state
                self.landing_frame = 0



    def move(self):
        global message, end_game, time_since_boost,score

        #Add boost_time when on ground
        if self.boost_time <= 60 and self.on_ground:
            self.boost_time += 1

        _scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        #move if velocity is not bigger then max speed
        if key[pygame.K_a]:
            if self.on_ground:
                if -self.vel_x < self.max_speed:
                    self.vel_x -= self.acceleration
            else:
                if -self.vel_x < self.max_speed:
                    self.vel_x -= self.air_speed
            self.flip = True
        if key[pygame.K_d]:
            if self.on_ground:
                if self.vel_x < self.max_speed:
                    self.vel_x += self.acceleration
            else:
                if self.vel_x < self.max_speed:
                    self.vel_x += self.air_speed
            self.flip = False
        if key[pygame.K_SPACE]:
            if self.on_ground and not self.space_held:
                if self.boost_time <= self.PERFECT_TIME:
                    jump_boost = self.PERFECT_BOOST
                    perfect_jump_sound.play()
                    message = "PERFECT"
                    time_since_boost = 0
                elif self.boost_time <= self.GREAT_BOOST:
                    jump_boost = self.GREAT_BOOST
                    great_jump_sound.play()
                    message = "GREAT"
                    time_since_boost = 0
                elif self.boost_time <= self.NICE_TIME:
                    jump_boost = self.NICE_BOOST
                    nice_jump_sound.play()
                    message = "Nice"
                    time_since_boost = 0
                else:
                    basic_jump_sound.play()
                    jump_boost = 1

                self.vel_y -= int(self.jump_speed * jump_boost)
                self.boost_time = 0
            # Mark space as held
            self.space_held = True
        else:
            if self.on_ground and self.vel_x == 0:
                self.change_state("standing")

            self.space_held = False

        #suspect we are falling
        self.on_ground = False

        #gravity
        self.vel_y += GRAVITY
        dy += self.vel_y


        # check collision with left wall
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        # check collision with right wall
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        # check collision with ground
        if self.rect.top + dy > SCREEN_HEIGHT:
            end_game = True

        # check collision with platform
        for p in platform_list:
            # y collision
            if p.rect.colliderect(self.rect.x , self.rect.y + dy, self.rect.width, self.rect.height):
                if self.rect.bottom <= p.rect.top:
                    self.on_ground = True
                    dy = p.rect.top - self.rect.bottom
                    # friction works on the ground
                    if self.vel_x > 0:
                        if self.vel_x != 0:
                            if self.vel_x < p.friction:
                                self.vel_x = 0
                            else:
                                self.vel_x -= p.friction
                    else:
                        if self.vel_x != 0:
                            if self.vel_x > -p.friction:
                                self.vel_x = 0
                            else:
                                self.vel_x += p.friction

        dx += self.vel_x

        #check SCROLL_THRESH collision
        if self.rect.top <= SCROLL_THRESHOLD:
            #only when jumping
            if self.vel_y < 0:
                _scroll = -dy



        #update position
        self.rect.x += dx
        self.rect.y += dy + _scroll
        self.absolute_y += dy

        #dont speed up when on ground
        if self.on_ground:
            self.vel_y = 0


        if not self.on_ground and self.state != "falling" and self.vel_y <= 0:
            self.change_state("jumping")
        if not self.on_ground and self.vel_y > 0:
            self.change_state("falling")
        if not self.on_ground and self.state == "falling" and self.vel_y == 0:
            self.change_state("landing")
        if self.on_ground and self.vel_x != 0:
            self.change_state("walking")
        if self.on_ground and self.vel_x == 0:
            self.change_state("standing")

        if self.absolute_y < self.max_y:
            score += abs(self.absolute_y - self.max_y)
            self.max_y = self.absolute_y

        return _scroll

#Platform class
class Platform:
    def __init__(self, x, y,width,friction,speed, image,color):
        self.color = color
        self.image = image
        self.rect = pygame.Rect(x, y, width, PLATFORM_HEIGHT)
        self.width = width
        self.rect.x = x
        self.rect.y = y
        self.friction = friction
        self.speed = speed
        self.direction = "right"

    def draw(self):
        scaled_image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        scaled_image.set_colorkey(BLACK)
        screen.blit(scaled_image, self.rect)

        # pygame.draw.rect(screen, self.color, self.rect)

    def update(self, _scroll):
        self.rect.y += _scroll

        if self.rect.top > SCREEN_HEIGHT:
            try:
                platform_list.remove(self)
            except ValueError:
                pass  # Platform might already be removed, avoid crashes

    def move(self):
        dx = 0

        if self.direction == "right":
            dx = self.speed
        else:
            dx = -self.speed

        if self.rect.right == SCREEN_WIDTH:
            self.direction = "left"
            dx = -self.speed
        if self.rect.left == 0:
            self.direction = "right"
            dx = self.speed
        if self.direction == "right" and self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        if self.direction == "left" and self.rect.left + dx < 0:
            dx = -self.rect.left

        self.rect.x += dx

class NormalPlatform(Platform):
    def __init__(self, x, y,width, image):
        super().__init__(x, y,width,1,0, image,BLACK)

class MovingPlatform(Platform):
    def __init__(self, x, y,width, image):
        super().__init__(x, y,width,1,2, image,GRAY)

class FastPlatform(Platform):
    def __init__(self, x, y,width, speed,image):
        super().__init__(x, y,width,1,speed, image,RED)

class IcyPlatform(Platform):
    def __init__(self, x, y, width, image):
        super().__init__(x, y, width, 0, 1, image,BLUE)

class StickyPlatform(Platform):
    def __init__(self, x, y, width, speed, image):
        super().__init__(x, y, width, 100, speed, image,GREEN)



def draw_platforms():
    global platform,score
    while len(platform_list) < MAX_PLATFORM:
        speed = random.randint(6,10)
        p_width = random.randint(int(0.1 * SCREEN_WIDTH), int(0.2 * SCREEN_WIDTH))
        p_x = random.randint(0, SCREEN_WIDTH - p_width)
        p_y = platform.rect.y - random.randint(MIN_PLATFORM_H, MAX_PLATFORM_H)

        num = random.random()

        # if num <= 1 - (score // EASY_BORDER):
        #     platform = NormalPlatform(p_x, p_y, p_width, log)
        # elif num <= 1 - (score // EASY_BORDER):
        #     platform = StickyPlatform(p_x, p_y,p_width, 0,sticky)
        # elif num <= 1 - (score // EASY_BORDER):
        #     platform = FastPlatform(p_x, p_y,p_width, rock)
        # elif num <= 1 - (score // EASY_BORDER):
        #     platform = IcyPlatform(p_x, p_y, p_width, icy)
        # else:
        #     platform = MovingPlatform(p_x, p_y,p_width,grass)
        if num <= 1 - (score / EASY_BORDER):
            platform = NormalPlatform(p_x, p_y, p_width, log)
        elif num <= 1 - (score / NORMAL_BORDER):
            platform = StickyPlatform(p_x, p_y,p_width, 0,sticky)
        elif num <= 1 - (score / HARD_BORDER):
            platform = MovingPlatform(p_x, p_y,p_width, rock)
        elif num <= 1 - (score / HARDCORE_BORDER):
            platform = IcyPlatform(p_x, p_y, p_width, icy)
        else:
            platform = FastPlatform(p_x, p_y,p_width,speed
                                    ,grass)


        platform_list.append(platform)

def start_game():
    global game_run, time_since_boost,scroll,end_game,platform,platform_list,score,message,click,player
    # player instance
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLATFORM_HEIGHT - PLAYER_HEIGHT)
    end_game = False
    game_run = True
    scroll = 0
    message = ""
    score = 0
    click = False
    time_since_boost = 0
    platform = None
    platform_list = []

    # platform instances
    platform = NormalPlatform(0, SCREEN_HEIGHT - PLATFORM_HEIGHT, SCREEN_WIDTH, log)
    platform_list.append(platform)

def reset_game():
    global platform_list,player,platform
    del platform_list
    del player
    del platform

def game():
    global game_run, time_since_boost, scroll, end_game, platform, platform_list, score, message, click, player,high_score_y
    start_game()

    while game_run:
        #draw background
        draw_bg()
        # pygame.draw.rect(screen.rect, WHITE)
        screen.fill(WHITE)
        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        myfont = pygame.font.SysFont(None, 48)

        clock.tick(FPS)
        #update player
        scroll = player.move()

        #update platforms
        for p in platform_list:
            p.update(scroll)

        #Add platform
        draw_platforms()

        #draw background
        #screen.blit(bg_image, (0, 0))



        for p in platform_list:
            p.move()
            p.draw()

        #draw players sprite
        player.draw_animation()
        player.draw()

        #game key handler
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pause()

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reset_game()
                main_menu("SKY JUMP")

        #if fallen out of the world
        if end_game:
            reset_game()
            main_menu("GAME OVER")

        # render text
        score_message = "Score " + str(score)
        score_message_width, score_message_height = myfont.size(score_message)
        draw_text_to_left(score_message, myfont, BLACK, screen, 10,  10)

        if time_since_boost <= FPS * 2:
            message_width, message_height = myfont.size(message)
            draw_text_to_left(message, myfont, BLACK, screen, 10, score_message_height + 10 )
            time_since_boost += 1
        #
        # pygame.draw.line(screen, RED, (0, high_score_y), (SCREEN_WIDTH, high_score_y), 5)
        # high_score_y +=  scroll

        #update display window
        pygame.display.update()

def draw_text(text,font,color, surface,x,y):
    text_obj = font.render(text, True, color)
    textrect = text_obj.get_rect()
    textrect.center = (x, y)
    surface.blit(text_obj, textrect)

    return textrect

def draw_text_to_left(text,font,color, surface,x,y):
    text_obj = font.render(text, True, color)
    textrect = text_obj.get_rect()
    textrect.left = x
    textrect.top = y
    surface.blit(text_obj, textrect)

def create_btn(btn_y,text,font,text_color,btn_color):
    text_width, text_height = font.size(text)
    button = pygame.Rect(0,0 , text_width + 10, text_height + 10)
    button.center = (SCREEN_WIDTH//2,btn_y)

    pygame.draw.rect(screen, btn_color, button)
    draw_text(text, font, text_color, screen, button.centerx, button.centery)

    return button

def main_menu(title):
    global main_menu_run,click,score
    main_menu_run = True
    click = False
    while main_menu_run:

        screen.fill(WHITE)

        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        h1_font = pygame.font.SysFont(None, 48)
        h2_font = pygame.font.SysFont(None, 32)


        title_width, title_height = h1_font.size(title)
        title_rect = draw_text(title, h1_font, BLACK, screen, SCREEN_WIDTH / 2, title_height + 70)

        if title == "GAME OVER":
            draw_text("Score: " + str(score), h2_font, BLACK, screen, SCREEN_WIDTH / 2, title_rect.bottom + 20)


        button_1 = create_btn(SCREEN_HEIGHT//2,"PLAY",h1_font,WHITE,BLACK)


        mx,my = pygame.mouse.get_pos()


        if button_1.collidepoint((mx,my)):
            if click:
                main_menu_run = False
                game()

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    main_menu_run = False
                    game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #update clock
        clock.tick(FPS)
        #update display window
        pygame.display.update()

def pause():
    global pause_run,click
    pause_run = True
    click = False
    while pause_run:

        font = pygame.font.SysFont(None, 48)
        button_1 = create_btn(SCREEN_HEIGHT//2,"PAUSE",font,WHITE,RED)

        mx, my = pygame.mouse.get_pos()

        if button_1.collidepoint((mx,my)):
            if click:
                pause_run = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu("SKY JUMP")
                if event.key == pygame.K_RETURN:
                    pause_run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        #update clock
        clock.tick(FPS)
        #update display window
        pygame.display.update()

main_menu("SKY JUMP")

#end game
pygame.mixer.music.stop()
nature_background_music.stop()
pygame.quit()