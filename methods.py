import pygame


class SpriteSheet:

    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image

    def get_image_left(self, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image = pygame.transform.flip(image, True, False)
        image.set_colorkey(color)
        return image

    def animation_list(self, num_frames, side="RIGHT"):
        temp_list = []
        for i in range(num_frames):
            if side == "RIGHT":
                temp_list.append(self.get_image(i, 24, 24, 3, (0, 0, 0)))
            else:
                temp_list.append(self.get_image_left(i, 24, 24, 3, (0, 0, 0)))
        return temp_list
