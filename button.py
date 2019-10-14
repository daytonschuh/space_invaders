import pygame.font


class Button:

    def __init__(self, screen, msg, rectx, recty):
        """ Initialize button attributes. """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 230, 50
        self.button_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 60)

        # Build the button's rect object and position it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = rectx
        self.rect.y = recty

        # The button message only needs to be prepped once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """ Turn msg into a rendered image and center text on the button. """
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """ Draw blank button, then draw message. """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
