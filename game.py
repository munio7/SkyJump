import sys
import pygame
import random
from platform import Platform
from player import Player


class NormalPlatform(Platform):
    def __init__(self, x, y, width, image,game):
        super().__init__(game,x, y, width, 1, 0, image,game.BLACK)


class MovingPlatform(Platform):
    def __init__(self, x, y, width, image,game):
        super().__init__(game,x, y, width, 1, 2, image, game.GRAY)


class FastPlatform(Platform):
    def __init__(self, x, y, width, speed, image,game):
        super().__init__(game,x, y, width, 1, speed, image, game.RED)


class IcyPlatform(Platform):
    def __init__(self, x, y, width, image,game):
        super().__init__(game,x, y, width, 0, 1, image, game.BLUE)


class StickyPlatform(Platform):
    def __init__(self, x, y, width, speed, image,game):
        super().__init__(game,x, y, width, 100, speed, image, game.GREEN)


class Game:

    def __init__(self):
    
        #init pygame

        pygame.init()
        self.UI = UI(self)
        
        #init mixerD
        pygame.mixer.init()
        
        #init music/sounds
        pygame.mixer.music.load('assets/sounds/main_background_music.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        
        nature_background_music = pygame.mixer.Sound('assets/sounds/nature_background_music.mp3')
        nature_background_music.set_volume(0.1)
        nature_background_music.play(loops=-1)
        
        self.basic_jump_sound = pygame.mixer.Sound('assets/sounds/basic_jump.mp3')
        self.basic_jump_sound.set_volume(0.3)
        
        self.nice_jump_sound = pygame.mixer.Sound('assets/sounds/nice_jump.mp3')
        self.nice_jump_sound.set_volume(0.3)
        
        self.great_jump_sound = pygame.mixer.Sound('assets/sounds/great_jump.mp3')
        self.great_jump_sound.set_volume(0.3)
        
        self.perfect_jump_sound = pygame.mixer.Sound('assets/sounds/perfect_jump.mp3')
        self.perfect_jump_sound.set_volume(0.3)
        
        #set frame rate
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        #colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.GRAY = (127, 127, 127)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        
        
        #game loop
        self.game_run = True
        self.pause_run = True
        self.main_menu_run = True
        
        #game window
        self.SCREEN_WIDTH = 576
        self.SCREEN_HEIGHT = 600
        
        #create game window
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        #game const
        self.SCROLL_THRESHOLD = self.SCREEN_HEIGHT // 4
        self.GRAVITY = 1
        self.MIN_PLATFORM_H = 110
        self.MAX_PLATFORM_H = 120
        self.MAX_PLATFORM = self.SCREEN_HEIGHT // self.MAX_PLATFORM_H + 1
        self.SCALE = 1
        self.HIGH_SCORE = 200
        self.EASY_BORDER = 2000
        self.NORMAL_BORDER = 4000
        self.HARD_BORDER = 6000
        self.HARDCORE_BORDER = 10000
        
        
        #game variables
        self.end_game = False
        self.scroll = 0
        self.message = ""
        self.score = 0
        self.click = False
        self.time_since_boost = 0
        self.platform = None
        self.platform_list = []
        self.high_score_y = self.SCREEN_HEIGHT - self.HIGH_SCORE
        
        #player const
        self.PLAYER_WIDTH = 44
        self.PLAYER_HEIGHT = 75
        self.PLAYER_ACCELERATION = 2

        self.player = None
        
        #platform const
        self.PLATFORM_HEIGHT = 20

        pygame.display.set_caption("SkyJump")
        
        self.bg_image = pygame.image.load("assets/background.png").convert_alpha()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        #platforms
        self.log = pygame.image.load("assets/platforms/log.png").convert_alpha()
        self.icy = pygame.image.load("assets/platforms/icy.png").convert_alpha()
        self.rock = pygame.image.load("assets/platforms/rock.png").convert_alpha()
        self.sticky = pygame.image.load("assets/platforms/sticky.png").convert_alpha()
        self.grass = pygame.image.load("assets/platforms/grass.png").convert_alpha()
        
        #background
        bg_images = []
        for i in range(1, 5):
            bg_image = pygame.image.load("assets/background/" "plan_" + str(i) + ".png").convert_alpha()
            bg_images.append(bg_image)
        
    def draw_bg(self):
        for bg_image in self.bg_images:
            self.screen.blit(bg_image, (0, self.SCREEN_HEIGHT - 324))

    def draw_platforms(self):
        while len(self.platform_list) < self.MAX_PLATFORM:
            speed = random.randint(6,10)
            p_width = random.randint(int(0.1 * self.SCREEN_WIDTH), int(0.2 * self.SCREEN_WIDTH))
            p_x = random.randint(0, self.SCREEN_WIDTH - p_width)
            p_y = self.platform.rect.y - random.randint(self.MIN_PLATFORM_H, self.MAX_PLATFORM_H)
    
            num = random.random()

            if num <= 1 - (self.score / self.EASY_BORDER):
                self.platform = NormalPlatform(p_x, p_y, p_width, self.log,self)
            elif num <= 1 - (self.score / self.NORMAL_BORDER):
                self.platform = StickyPlatform(p_x, p_y,p_width, 0,self.sticky,self)
            elif num <= 1 - (self.score / self.HARD_BORDER):
                self.platform = MovingPlatform(p_x, p_y,p_width, self.rock,self)
            elif num <= 1 - (self.score / self.HARDCORE_BORDER):
                self.platform = IcyPlatform(p_x, p_y, p_width, self.icy,self)
            else:
                self.platform = FastPlatform(p_x, p_y,p_width,speed,self.grass,self)
    
    
            self.platform_list.append(self.platform)
    
    def start_game(self):
        # player instance
        self.player = Player(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - self.PLATFORM_HEIGHT - self.PLAYER_HEIGHT,self)

        self.end_game = False
        self.game_run = True
        self.scroll = 0
        self.message = ""
        self.score = 0
        self.click = False
        self.time_since_boost = 0
        self.platform = None
        self.platform_list = []
    
        # platform instances
        self.platform = NormalPlatform(0, self.SCREEN_HEIGHT - self.PLATFORM_HEIGHT, self.SCREEN_WIDTH, self.log,self)
        self.platform_list.append(self.platform)
    
    def reset_game(self):
        del self.platform_list
        del self.player
        del self.platform
    
    def game(self):
        self.start_game()
    
        while self.game_run:
            #draw background
            # self.draw_bg()
            # pygame.draw.rect(screen.rect, WHITE)
            self.screen.fill(self.WHITE)
            # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
            myfont = pygame.font.SysFont(None, 48)
    
            self.clock.tick(self.FPS)
            #update player
            self.scroll = self.player.move()
    
            #update platforms
            for p in self.platform_list:
                p.update(self.scroll)
    
            #Add platform
            self.draw_platforms()
    
            for p in self.platform_list:
                p.move()
                p.draw()
    
            #draw players sprite
            self.player.draw_animation()
            self.player.draw()
    
            #game key handler
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.UI.pause()
    
            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.reset_game()
                    self.UI.main_menu("SKY JUMP")
    
            #if fallen out of the world
            if self.end_game:
                self.reset_game()
                self.UI.main_menu("GAME OVER")
    
            # render text
            score_message = "Score " + str(self.score)
            score_message_width, score_message_height = myfont.size(score_message)
            self.UI.draw_text_to_left(score_message, myfont, self.BLACK, self.screen, 10,  10)
    
            if self.time_since_boost <= self.FPS * 2:
                # message_width, message_height = myfont.size(self.message)
                self.UI.draw_text_to_left(self.message, myfont, self.BLACK, self.screen, 10, score_message_height + 10 )
                self.time_since_boost += 1
    
            #update display window
            pygame.display.update()
    
    
    
class UI:
    def __init__(self, game):
        self.game = game

    
    
    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        textrect = text_obj.get_rect()
        textrect.center = (x, y)
        surface.blit(text_obj, textrect)

        return textrect

    def draw_text_to_left(self,text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        textrect = text_obj.get_rect()
        textrect.left = x
        textrect.top = y
        surface.blit(text_obj, textrect)

    def create_btn(self,btn_y, text, font, text_color, btn_color):
        game = self.game
        text_width, text_height = font.size(text)
        button = pygame.Rect(0, 0, text_width + 10, text_height + 10)
        button.center = (game.SCREEN_WIDTH // 2, btn_y)

        pygame.draw.rect(game.screen, btn_color, button)
        self.draw_text(text, font, text_color, game.screen, button.centerx, button.centery)

        return button

    def main_menu(self,title):
        game = self.game
        game.main_menu_run = True
        while game.main_menu_run:

            game.screen.fill(game.WHITE)

            # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
            h1_font = pygame.font.SysFont(None, 48)
            h2_font = pygame.font.SysFont(None, 32)

            title_width, title_height = h1_font.size(title)
            title_rect = self.draw_text(title, h1_font, game.BLACK, game.screen, game.SCREEN_WIDTH / 2, title_height + 70)

            if title == "GAME OVER":
                self.draw_text("Score: " + str(game.score), h2_font, game.BLACK, game.screen, game.SCREEN_WIDTH / 2, title_rect.bottom + 20)

            button_1 = self.create_btn(game.SCREEN_HEIGHT // 2, "PLAY", h1_font, game.WHITE, game.BLACK)

            mx, my = pygame.mouse.get_pos()

            if button_1.collidepoint((mx, my)):
                if game.click:
                    game.main_menu_run = False
                    game.game()

            game.click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:
                        game.main_menu_run = False
                        game.game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        game.click = True

            # update clock
            game.clock.tick(game.FPS)
            # update display window
            pygame.display.update()

    def pause(self):
        game = self.game

        game.pause_run = True
        while game.pause_run:

            font = pygame.font.SysFont(None, 48)
            button_1 = self.create_btn(game.SCREEN_HEIGHT // 2, "PAUSE", font, game.WHITE, game.RED)

            mx, my = pygame.mouse.get_pos()

            if button_1.collidepoint((mx, my)):
                if game.click:
                    game.pause_run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu("SKY JUMP")
                    if event.key == pygame.K_RETURN:
                        game.pause_run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        game.click = True

            # update clock
            game.clock.tick(game.FPS)
            # update display window
            pygame.display.update()
