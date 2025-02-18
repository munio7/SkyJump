import pygame

#player class
class Player:


    def __init__(self, x, y,game):
        self.game = game

        self.state = "standing"

        self.idle_image = pygame.image.load("assets/player_sprites/Idle.png").convert_alpha()
        self.idle_image = pygame.transform.scale(self.idle_image, (game.PLAYER_WIDTH * game.SCALE, game.PLAYER_HEIGHT * game.SCALE))

        self.falling_image = pygame.image.load("assets/player_sprites/Falling.png").convert_alpha()
        self.falling_image = pygame.transform.scale(self.falling_image, (game.PLAYER_WIDTH * game.SCALE, game.PLAYER_HEIGHT * game.SCALE))

        self.landing_sheet = pygame.image.load('assets/player_sprites/landing_sheet.png').convert_alpha()
        self.landing_frame = 0
        self.LANDING_STEPS = 3
        self.LANDING_ANIMATION_COOLDOWN = 100
        self.landing_last_update = pygame.time.get_ticks()
        self.landing_a_list = self.load_images(self.landing_sheet, self.LANDING_STEPS, game.SCALE)

        self.walk_sheet = pygame.image.load('assets/player_sprites/walk_sheet.png').convert_alpha()
        self.walk_frame = 0
        self.WALK_STEPS = 7
        self.WALK_ANIMATION_COOLDOWN = 100
        self.walk_last_update = pygame.time.get_ticks()
        self.walk_a_list = self.load_images(self.walk_sheet,self.WALK_STEPS ,game.SCALE)

        self.jump_sheet = pygame.image.load("assets/player_sprites/jump_sheet.png").convert_alpha()
        self.jump_frame = 0
        self.JUMP_STEPS = 7
        self.JUMP_ANIMATION_COOLDOWN = 100
        self.jump_last_update = pygame.time.get_ticks()
        self.jump_a_list = self.load_images(self.jump_sheet, self.JUMP_STEPS, game.SCALE)

        self.air_speed = 1
        self.max_speed = 10
        self.acceleration = game.PLAYER_ACCELERATION
        self.jump_speed = 20

        self.rect = pygame.Rect(0, 0, game.PLAYER_WIDTH * game.SCALE, game.PLAYER_HEIGHT * game.SCALE)
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
        game = self.game

        image = pygame.Surface((game.PLAYER_WIDTH, game.PLAYER_HEIGHT)).convert_alpha()
        image.blit(sheet, (0, 0), ((game.PLAYER_WIDTH * frame), 0, game.PLAYER_WIDTH, game.PLAYER_HEIGHT))
        image = pygame.transform.scale(image, (game.PLAYER_WIDTH * scale, game.PLAYER_HEIGHT * scale))
        image.set_colorkey(color_key)

        return image

    def load_images(self,sheet, steps,scale):
        a_list = []
        for x in range(steps):
            a_list.append(self.get_frame_img(x,sheet,scale,self.game.GRAY))
        return a_list

    def get_image(self,sheet, color_key):
        game = self.game

        image = pygame.Surface((game.PLAYER_WIDTH, game.PLAYER_HEIGHT)).convert_alpha()
        image.blit(sheet, (0, 0))
        image.set_colorkey(color_key)
        return image

    def draw(self):
        game = self.game

        flipped_current_img = pygame.transform.flip(self.current_image,self.flip,False)
        flipped_current_img.set_colorkey(game.GRAY)
        game.screen.blit(flipped_current_img, self.rect)

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
        game = self.game

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
                    game.perfect_jump_sound.play()
                    game.message = "PERFECT"
                    game.time_since_boost = 0
                elif self.boost_time <= self.GREAT_BOOST:
                    jump_boost = self.GREAT_BOOST
                    game.great_jump_sound.play()
                    game.message = "GREAT"
                    game.time_since_boost = 0
                elif self.boost_time <= self.NICE_TIME:
                    jump_boost = self.NICE_BOOST
                    game.nice_jump_sound.play()
                    game.message = "Nice"
                    game.time_since_boost = 0
                else:
                    game.basic_jump_sound.play()
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
        self.vel_y += game.GRAVITY
        dy += self.vel_y


        # check collision with left wall
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        # check collision with right wall
        if self.rect.right + dx > game.SCREEN_WIDTH:
            dx = game.SCREEN_WIDTH - self.rect.right
        # check collision with ground
        if self.rect.top + dy > game.SCREEN_HEIGHT:
            game.end_game = True

        # check collision with platform
        for p in game.platform_list:
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
        if self.rect.top <= game.SCROLL_THRESHOLD:
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
            game.score += abs(self.absolute_y - self.max_y)
            self.max_y = self.absolute_y

        return _scroll
