import math
import pygame
import random


class Ball:
    def __init__(self, surface: pygame.Surface):
        self.__surface = surface
        self.__radius = 15

        self.__angle = random.choice([random.uniform(- math.pi / 4, - math.pi / 10), random.uniform(math.pi / 10, math.pi / 4)])
        self.__x_velocity = self.__initial_x_velocity = random.choice([math.cos(self.__angle), -math.cos(self.__angle)])
        self.__y_velocity = self.__initial_y_velocity = random.choice([math.sin(self.__angle), -math.sin(self.__angle)])

        self.__speed = 3
        self.__starting_coords = self.__surface.get_width() // 2 - self.__radius, self.__surface.get_height() // 2 - self.__radius
        self.__circle = pygame.Rect(*self.__starting_coords, self.__radius * 2, self.__radius * 2)
        self.__color = "white"

    def reset_ball(self):
        self.__circle.x, self.__circle.y = self.__starting_coords
        self.__speed = 3
        self.__angle = random.choice(
            [random.uniform(- math.pi / 4, - math.pi / 10), random.uniform(math.pi / 10, math.pi / 4)])
        self.__x_velocity = random.choice([math.cos(self.__angle), -math.cos(self.__angle)])
        self.__y_velocity = random.choice([math.sin(self.__angle), -math.sin(self.__angle)])

    def randomize_angle(self):
        epsilon = 0.5
        adjustment = random.choice([0, 0.1, -0.1])
        if self.__initial_y_velocity - epsilon <= self.__y_velocity + adjustment <= self.__initial_y_velocity + epsilon:
            self.__y_velocity += adjustment

    def get_rect(self):
        return self.__circle

    def get_velocity(self):
        return self.__x_velocity, self.__y_velocity

    def get_width(self):
        return self.__radius * 2

    def get_speed(self):
        return self.__speed

    def increase_speed(self):
        if self.__speed < 25:
            self.__speed += 0.3

    def draw(self):
        pygame.draw.circle(self.__surface, self.__color, self.__circle.center, self.__radius)

    def invert_x_velocity(self):
        self.__x_velocity *= -1

    def invert_y_velocity(self):
        self.__y_velocity *= -1

    def move(self):
        self.__circle.x += self.__x_velocity * self.__speed
        self.__circle.y += self.__y_velocity * self.__speed
