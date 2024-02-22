import pygame

from ai.ai import AI
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
        self.__fps = 120
        self.__background_color = "black"
        self.__is_running = False
        self.__game_end = False

        # players
        self.__distance_from_border = 15
        player_starting_position = self.__distance_from_border, (self.__screen_size[1] - 100) // 2
        enemy_starting_position = self.__screen_size[0] - 30 - self.__distance_from_border, (
                self.__screen_size[1] - 100) // 2
        self.__player = Paddle(player_starting_position, self.__screen)
        self.__enemy = Paddle(enemy_starting_position, self.__screen)
        self.__ai_right = AI(self.__enemy)
        self.__ai_left = AI(self.__player)

        # ball
        self.__ball = Ball(self.__screen)
        self.__future_player1_position = self.__ai_left.predict_ball_position_left(self.__ball, self.__screen.get_width(), self.__screen.get_height(), self.__distance_from_border)
        self.__future_player2_position = self.__ai_right.predict_ball_position_right(self.__ball, self.__screen.get_width(), self.__screen.get_height(), self.__distance_from_border)

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
        if self.__game_end and keys[pygame.K_SPACE]:
            self.__game_end = False
            self.__ball.reset_ball()
            self.__future_player1_position = self.__ai_left.predict_ball_position_left(self.__ball, self.__screen.get_width(), self.__screen.get_height(), self.__distance_from_border)
            self.__future_player2_position = self.__ai_right.predict_ball_position_right(self.__ball, self.__screen.get_width(), self.__screen.get_height(), self.__distance_from_border)

    def __ball_collision(self):
        # paddle collision
        if self.__ball.get_rect().colliderect(self.__player.get_rect()) or self.__ball.get_rect().colliderect(
                self.__enemy.get_rect()):
            # front collision
            if (self.__ball.get_rect().x + self.__ball.get_speed() >= self.__player.get_rect().x + self.__player.get_width()
                    and self.__ball.get_rect().x + self.__ball.get_width() - self.__ball.get_speed() <= self.__enemy.get_rect().x):
                self.__ball.invert_x_velocity()
                self.__ball.increase_speed()
                # self.__ball.randomize_bounce_angle()

                self.__future_player1_position = self.__ai_left.predict_ball_position_left(self.__ball, self.__screen.get_width(), self.__screen.get_height(), self.__distance_from_border)
                self.__future_player2_position = self.__ai_right.predict_ball_position_right(self.__ball, self.__screen.get_width(), self.__screen.get_height(), self.__distance_from_border)

            # top and bottom collision
            else:
                self.__ball.invert_y_velocity()

        # collision with top and bottom screen bounds
        if self.__ball.get_rect().y <= 0 or self.__ball.get_rect().y >= self.__screen.get_height() - self.__ball.get_rect().height:
            self.__ball.invert_y_velocity()

            self.__future_player1_position = self.__ai_left.predict_ball_position_left(self.__ball, self.__screen.get_width(), self.__screen.get_height(), self.__distance_from_border)
            self.__future_player2_position = self.__ai_right.predict_ball_position_right(self.__ball, self.__screen.get_width(), self.__screen.get_height(), self.__distance_from_border)

    def __check_end_game(self):
        def display_text(text: str):
            text_surface = pygame.font.Font(None, 36).render(text, True, "white")
            text_rect = text_surface.get_rect(center=(self.__screen.get_width() // 2, self.__screen.get_height() // 2))
            self.__screen.blit(text_surface, text_rect)

            space_prompt = pygame.font.Font(None, 24).render("Press space to play again", True, "white")
            space_rect = space_prompt.get_rect(
                center=(self.__screen.get_width() // 2, text_rect.y + text_rect.height + 20))
            self.__screen.blit(space_prompt, space_rect)

        if self.__ball.get_rect().x + self.__ball.get_width() <= 0:
            display_text("Player 2 wins!")
            self.__game_end = True
        if self.__ball.get_rect().x >= self.__screen.get_width():
            self.__game_end = True
            display_text("Player 1 wins!")

    def run(self):
        self.__is_running = True
        while self.__is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__is_running = False

            self.__screen.fill(self.__background_color)
            self.__player.draw()
            self.__enemy.draw()
            self.__ball.draw()

            self.__future_player1_position = self.__ai_left.predict_ball_position_left(self.__ball,
                                                                                       self.__screen.get_width(),
                                                                                       self.__screen.get_height(),
                                                                                       self.__distance_from_border)
            self.__future_player2_position = self.__ai_right.predict_ball_position_right(self.__ball,
                                                                                         self.__screen.get_width(),
                                                                                         self.__screen.get_height(),
                                                                                         self.__distance_from_border)

            # if you want to play yourself just comment the next two lines
            self.__ai_left.move_paddle(self.__future_player1_position)
            self.__ai_right.move_paddle(self.__future_player2_position)

            if not self.__game_end:
                self.__ball.move()
            self.__keypress_actions()

            self.__ball_collision()
            self.__check_end_game()

            pygame.display.flip()

            self.__clock.tick(self.__fps)

        pygame.quit()
