import math
import pygame
import random


class Ball:
    def __init__(self, surface: pygame.Surface):
        self.__surface = surface
        self.__radius = 15

        angle = random.choice([random.uniform(- math.pi / 4, - math.pi / 10), random.uniform(math.pi / 10, math.pi / 4)])
        self.__x_velocity = random.choice([math.cos(angle), -math.cos(angle)])
        self.__y_velocity = random.choice([math.sin(angle), -math.sin(angle)])

        self.__speed = 5
        starting_coords = self.__surface.get_width() // 2 - self.__radius, self.__surface.get_height() // 2 - self.__radius
        self.__circle = pygame.Rect(*starting_coords, self.__radius * 2, self.__radius * 2)
        self.__color = "white"

    def get_rect(self):
        return self.__circle

    def draw(self):
        pygame.draw.circle(self.__surface, self.__color, self.__circle.center, self.__radius)

    def invert_x_velocity(self):
        self.__x_velocity *= -1

    def invert_y_velocity(self):
        self.__y_velocity *= -1

    def move(self):
        self.__circle.x += self.__x_velocity * self.__speed
        self.__circle.y += self.__y_velocity * self.__speed
