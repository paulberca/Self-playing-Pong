class AI:
    def __init__(self, paddle):
        self.__paddle = paddle

    def predict_ball_position_right(self, ball, screen_width, screen_height, distance_form_border):
        ball_rect = ball.get_rect().copy()
        ball_velocity_x, ball_velocity_y = ball.get_velocity()
        ball_speed = ball.get_speed()

        repetitions = 0
        while ball_rect.x < screen_width - self.__paddle.get_width():    # this only works for the left paddle
            ball_rect.x += ball_velocity_x * ball_speed
            ball_rect.y += ball_velocity_y * ball_speed

            if ball_rect.y <= 0 or ball_rect.y >= screen_height:
                ball_velocity_y = -ball_velocity_y

            if ball_rect.x <= self.__paddle.get_width() + distance_form_border:
                ball_velocity_x = -ball_velocity_x

            repetitions += 1
            if repetitions > 10000:
                break

        return ball_rect.y

    def predict_ball_position_left(self, ball, screen_width, screen_height, distance_form_border):
        ball_rect = ball.get_rect().copy()
        ball_velocity_x, ball_velocity_y = ball.get_velocity()
        ball_speed = ball.get_speed()

        repetitions = 0
        while ball_rect.x > distance_form_border + self.__paddle.get_width():  # this only works for the left paddle
            ball_rect.x += ball_velocity_x * ball_speed
            ball_rect.y += ball_velocity_y * ball_speed

            if ball_rect.y <= 0 or ball_rect.y >= screen_height:
                ball_velocity_y = -ball_velocity_y

            if ball_rect.x >= screen_width - self.__paddle.get_width():
                ball_velocity_x = -ball_velocity_x

            repetitions += 1
            if repetitions > 10000:
                break

        return ball_rect.y

    def move_paddle(self, future_ball_position):
        epsilon = 10
        if future_ball_position - epsilon > self.__paddle.get_rect().y + self.__paddle.get_height() // 2:
            self.__paddle.move("down")
        if future_ball_position + epsilon < self.__paddle.get_rect().y + self.__paddle.get_height() // 2:
            self.__paddle.move("up")
