import pygame.draw


class Paddle:
    def __init__(self, initial_coords: tuple, surface: pygame.Surface):
        self.__width = 30
        self.__height = 150
        self.__distance_from_border = 25
        self.__surface = surface
        self.__rect = pygame.Rect(*initial_coords, self.__width, self.__height)
        self.__speed = 6
        self.__color = "white"

    def get_rect(self):
        return self.__rect

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_speed(self):
        return self.__speed

    def draw(self):
        pygame.draw.rect(self.__surface, self.__color, self.__rect)

    def move(self, direction):
        if direction == "up" and self.__rect.y > 0:
            self.__rect.y -= self.__speed
        elif direction == "down" and self.__rect.y < self.__surface.get_height() - self.__height:
            self.__rect.y += self.__speed
