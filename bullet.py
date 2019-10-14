import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # a class to manage bullets fired from the ship
    def __init__(self, ai_settings, screen, source, source_name):
        # create a bullet object at the ship's current position
        super(Bullet, self).__init__()
        self.screen = screen

        # create a bullet rect at (0,0) and then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)
        self.source_name = source_name
        self.rect.centerx = source.rect.centerx
        if self.source_name == "alien":
            self.rect.bottom = source.rect.bottom
        elif self.source_name == "ship":
            self.rect.top = source.rect.top

        # store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        # move the bullet up the screen
        # update the decimal position of the bullet
        if self.source_name == "ship":
            self.y -= self.speed_factor
        elif self.source_name == "alien":
            self.y += (self.speed_factor / 2)
            # update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        # draw the bullet to the screen
        pygame.draw.rect(self.screen, self.color, self.rect)
