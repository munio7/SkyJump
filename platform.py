import pygame

#Platform class
class Platform:
    def __init__(self, game,x, y,width,friction,speed, image,color):
        self.game = game

        self.color = color
        self.image = image
        self.rect = pygame.Rect(x, y, width, game.PLATFORM_HEIGHT)
        self.width = width
        self.rect.x = x
        self.rect.y = y
        self.friction = friction
        self.speed = speed
        self.direction = "right"

    def draw(self):
        game = self.game

        scaled_image = pygame.transform.scale(self.image,(self.rect.width,self.rect.height))
        scaled_image.set_colorkey(game.BLACK)
        game.screen.blit(scaled_image, self.rect)

        # pygame.draw.rect(screen, self.color, self.rect)

    def update(self, _scroll):
        game = self.game

        self.rect.y += _scroll

        if self.rect.top > game.SCREEN_HEIGHT:
            try:
                game.platform_list.remove(self)
            except ValueError:
                pass  # Platform might already be removed, avoid crashes

    def move(self):
        game = self.game

        dx = 0

        if self.direction == "right":
            dx = self.speed
        else:
            dx = -self.speed

        if self.rect.right == game.SCREEN_WIDTH:
            self.direction = "left"
            dx = -self.speed
        if self.rect.left == 0:
            self.direction = "right"
            dx = self.speed
        if self.direction == "right" and self.rect.right + dx > game.SCREEN_WIDTH:
            dx = game.SCREEN_WIDTH - self.rect.right
        if self.direction == "left" and self.rect.left + dx < 0:
            dx = -self.rect.left

        self.rect.x += dx

