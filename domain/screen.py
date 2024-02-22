import pygame

from domain.ball import Ball
from domain.paddle import Paddle


class Screen:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")

        # the window
        self.__screen_size = 600, 400
        self.__screen = pygame.display.set_mode(self.__screen_size)
        self.__clock = pygame.time.Clock()
        self.__fps = 60
        self.__background_color = "black"

        # players
        self.__distance_from_border = 15
        player_starting_position = self.__distance_from_border, (self.__screen_size[1] - 100) // 2
        enemy_starting_position = self.__screen_size[0] - 30 - self.__distance_from_border, (self.__screen_size[1] - 100) // 2
        self.__player = Paddle(player_starting_position, self.__screen)
        self.__enemy = Paddle(enemy_starting_position, self.__screen)

        # ball
        self.__ball = Ball(self.__screen)

    def __keypress_actions(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.__player.move("up")
        if keys[pygame.K_s]:
            self.__player.move("down")
        if keys[pygame.K_UP]:
            self.__enemy.move("up")
        if keys[pygame.K_DOWN]:
            self.__enemy.move("down")

    def __ball_collision(self):
        if self.__ball.get_rect().colliderect(self.__player.get_rect()) or self.__ball.get_rect().colliderect(self.__enemy.get_rect()):
            self.__ball.invert_x_velocity()

        if self.__ball.get_rect().y <= 0 or self.__ball.get_rect().y >= self.__screen.get_height() - self.__ball.get_rect().height:
            self.__ball.invert_y_velocity()

    def run(self):
        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

            self.__screen.fill(self.__background_color)
            self.__player.draw()
            self.__enemy.draw()
            self.__ball.draw()

            self.__ball.move()
            self.__keypress_actions()

            self.__ball_collision()

            pygame.display.flip()

            self.__clock.tick(self.__fps)
