import pygame
import os
pygame.font.init()

# Константы.
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bashe game.")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

MAIN_FONT = pygame.font.SysFont('comicsans', WIDTH // 40)
WINNER_FONT = pygame.font.SysFont('comicsans', WIDTH // 10)

FPS = 60
HEAP_WIDTH, HEAP_HEIGHT = WIDTH // 4, HEIGHT // 2

HEAP_IMAGE = pygame.image.load(os.path.join('Data', 'Heap.png'))
PLAYER_HEAP = pygame.transform.scale(HEAP_IMAGE, (HEAP_WIDTH, HEAP_HEIGHT))

# Количество камней у игроков и сколько они хотят взять.
START_STONES = 15
PLAYER_CAN_GET_MAX = 3

STONES_LEFT = START_STONES
FIRST_PLAYER_STONES = 0
SECOND_PLAYER_STONES = 0

FIRST_PLAYER_GET_STONES = 1
SECOND_PLAYER_GET_STONES = 1

CURRENT_TURN = 1


# Класс для кнопок.
class Button:
    def __init__(self, width, height, message, inactive_color, active_color, freeze_color, action,
                 message_offset_x = 0, message_offset_y = 0):
        self.width = width
        self.height = height
        self.message = message
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.freeze_color = freeze_color
        self.action = action
        self.message_offset_x = message_offset_x
        self.message_offset_y = message_offset_y
        self.freeze = 0

    def draw(self, x, y):
        if not self.freeze:
            mouse_pos = pygame.mouse.get_pos()
            is_pressed = pygame.mouse.get_pressed()

            if x < mouse_pos[0] < x + self.width and y < mouse_pos[1] < y + self.height:
                pygame.draw.rect(WIN, self.active_color, pygame.Rect((x, y), (self.width, self.height)))
                text = MAIN_FONT.render(self.message, True, self.inactive_color)
                WIN.blit(text, (x + self.message_offset_x, y + self.message_offset_y))

                if is_pressed[0]:
                    self.action()
                    pygame.time.delay(200)

            else:
                pygame.draw.rect(WIN, self.inactive_color, pygame.Rect((x, y), (self.width, self.height)))
                text = MAIN_FONT.render(self.message, True, self.active_color)
                WIN.blit(text, (x + self.message_offset_x, y + self.message_offset_y))
        else:
            pygame.draw.rect(WIN, self.freeze_color, pygame.Rect((x, y), (self.width, self.height)))
            text = MAIN_FONT.render(self.message, True, self.active_color)
            WIN.blit(text, (x + self.message_offset_x, y + self.message_offset_y))


# Вспомогательная функция для отрисовки кнопок.
def get_width_text(font, text):
    rendered_text = font.render(text, True, WHITE)
    return rendered_text.get_width()


# Отрисовка.
def draw_window(first_player_heap, second_player_heap, main_heap,
                first_player_plus_b, first_player_minus_b,
                second_player_plus_b, second_player_minus_b,
                next_player_turn):
    WIN.fill(WHITE)

    # Отрисуем текст.
    player_1_text = MAIN_FONT.render("Player 1", True, BLACK)
    player_2_text = MAIN_FONT.render("Player 2", True, BLACK)
    get_N_things_text = MAIN_FONT.render("Get N things:", True, BLACK)

    WIN.blit(player_1_text, (get_N_things_text.get_width() // 2 - player_1_text.get_width() // 2, 0))
    WIN.blit(player_2_text, (WIDTH - get_N_things_text.get_width() // 2 - player_2_text.get_width() // 2,  0))
    WIN.blit(get_N_things_text, (0, player_1_text.get_height()))
    WIN.blit(get_N_things_text, (WIDTH - get_N_things_text.get_width(), player_2_text.get_height()))

    # Отрисуем кнопки.
    first_player_plus_b.draw(0, player_1_text.get_height() + get_N_things_text.get_height())
    first_player_minus_b.draw(get_N_things_text.get_width() - first_player_minus_b.width,
                              player_1_text.get_height() + get_N_things_text.get_height())
    second_player_plus_b.draw(WIDTH - get_N_things_text.get_width(), player_2_text.get_height() + get_N_things_text.get_height())
    second_player_minus_b.draw(WIDTH - second_player_minus_b.width,
                               player_2_text.get_height() + get_N_things_text.get_height())
    next_player_turn.draw(WIDTH//2 - next_player_turn.width//2, 0)

    # Отрисуем кучи камней
    WIN.blit(PLAYER_HEAP, (first_player_heap.x, first_player_heap.y -
                           first_player_heap.height * (FIRST_PLAYER_STONES / START_STONES)))
    WIN.blit(PLAYER_HEAP, (second_player_heap.x, second_player_heap.y -
                           second_player_heap.height * (SECOND_PLAYER_STONES / START_STONES)))
    WIN.blit(PLAYER_HEAP, (main_heap.x, main_heap.y +
                           main_heap.height * (1 - STONES_LEFT / START_STONES)))

    # Отрисуем количества камней.
    first_player_stones_num_text = MAIN_FONT.render(str(FIRST_PLAYER_STONES), True, WHITE)
    second_player_stones_num_text = MAIN_FONT.render(str(SECOND_PLAYER_STONES), True, WHITE)
    first_player_stones_get_num_text = MAIN_FONT.render(str(FIRST_PLAYER_GET_STONES), True, WHITE)
    second_player_stones_get_num_text = MAIN_FONT.render(str(SECOND_PLAYER_GET_STONES), True, WHITE)
    stones_left_text = MAIN_FONT.render(str(STONES_LEFT), True, WHITE)

    text_rect = pygame.draw.rect(WIN, BLACK,
                                 (first_player_heap.x + first_player_heap.width // 2 - first_player_stones_num_text.get_width() // 2,
                                 HEIGHT - first_player_stones_num_text.get_height(),
                                 first_player_stones_num_text.get_width(),
                                 first_player_stones_num_text.get_height()))
    WIN.blit(first_player_stones_num_text, (text_rect.x, text_rect.y))
    text_rect = pygame.draw.rect(WIN, BLACK,
                                 (second_player_heap.x + second_player_heap.width // 2 - second_player_stones_num_text.get_width() // 2,
                                 HEIGHT - second_player_stones_num_text.get_height(),
                                 second_player_stones_num_text.get_width(),
                                 second_player_stones_num_text.get_height()))
    WIN.blit(second_player_stones_num_text, (text_rect.x, text_rect.y))
    text_rect = pygame.draw.rect(WIN, BLACK,
                                 (get_N_things_text.get_width() // 2 - first_player_stones_get_num_text.get_width() // 2,
                                 player_1_text.get_height() + get_N_things_text.get_height(),
                                 first_player_stones_get_num_text.get_width(),
                                 first_player_stones_get_num_text.get_height()))
    WIN.blit(first_player_stones_get_num_text, (text_rect.x, text_rect.y))
    text_rect = pygame.draw.rect(WIN, BLACK,
                                 (WIDTH - get_N_things_text.get_width() // 2 - second_player_stones_get_num_text.get_width() // 2,
                                 player_2_text.get_height() + get_N_things_text.get_height(),
                                 second_player_stones_get_num_text.get_width(),
                                 second_player_stones_get_num_text.get_height()))
    WIN.blit(second_player_stones_get_num_text, (text_rect.x, text_rect.y))
    text_rect = pygame.draw.rect(WIN, BLACK,
                                 (main_heap.x + main_heap.width // 2 - stones_left_text.get_width() // 2,
                                 HEIGHT - stones_left_text.get_height(),
                                 stones_left_text.get_width(),
                                 stones_left_text.get_height()))
    WIN.blit(stones_left_text, (text_rect.x, text_rect.y))

    # Обновим отрисовку.
    pygame.display.update()


def draw_win_text(text):
    draw_text = WINNER_FONT.render(text, True, GREEN)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


# Действия кнопок.
def first_plus_action():
    global FIRST_PLAYER_GET_STONES
    if FIRST_PLAYER_GET_STONES < PLAYER_CAN_GET_MAX:
        FIRST_PLAYER_GET_STONES += 1


def first_minus_action():
    global FIRST_PLAYER_GET_STONES
    if FIRST_PLAYER_GET_STONES > 1:
        FIRST_PLAYER_GET_STONES -= 1


def second_plus_action():
    global SECOND_PLAYER_GET_STONES
    if SECOND_PLAYER_GET_STONES < PLAYER_CAN_GET_MAX:
        SECOND_PLAYER_GET_STONES += 1


def second_minus_action():
    global SECOND_PLAYER_GET_STONES
    if SECOND_PLAYER_GET_STONES > 1:
        SECOND_PLAYER_GET_STONES -= 1


def next_turn_action():
    global CURRENT_TURN, STONES_LEFT

    if CURRENT_TURN == 1:
        global FIRST_PLAYER_STONES
        FIRST_PLAYER_STONES += FIRST_PLAYER_GET_STONES
        STONES_LEFT -= FIRST_PLAYER_GET_STONES
        STONES_LEFT = 0 if STONES_LEFT < 0 else STONES_LEFT
    else:
        global SECOND_PLAYER_STONES
        SECOND_PLAYER_STONES += SECOND_PLAYER_GET_STONES
        STONES_LEFT -= SECOND_PLAYER_GET_STONES
        STONES_LEFT = 0 if STONES_LEFT < 0 else STONES_LEFT

    CURRENT_TURN = 1 if CURRENT_TURN == 2 else 2



# Главный цикл + логика.
def main():
    # Три кучи.
    first_player_heap = pygame.Rect(0, HEIGHT, HEAP_WIDTH, HEAP_HEIGHT)
    second_player_heap = pygame.Rect(WIDTH - HEAP_WIDTH, HEIGHT, HEAP_WIDTH, HEAP_HEIGHT)
    main_heap = pygame.Rect(WIDTH // 2 - HEAP_WIDTH // 2, HEIGHT - HEAP_HEIGHT, HEAP_WIDTH, HEAP_HEIGHT)

    # Все кнопки:
    first_player_plus_b = Button(MAIN_FONT.get_height(), MAIN_FONT.get_height(), "+",
                                 BLACK, WHITE, RED, first_plus_action,
                                 MAIN_FONT.get_height() // 2 - get_width_text(MAIN_FONT, "+") // 2)
    first_player_minus_b = Button(MAIN_FONT.get_height(), MAIN_FONT.get_height(), "-",
                                  BLACK, WHITE, RED, first_minus_action,
                                  MAIN_FONT.get_height() // 2 - get_width_text(MAIN_FONT, "-") // 2)
    second_player_plus_b = Button(MAIN_FONT.get_height(), MAIN_FONT.get_height(), "+",
                                  BLACK, WHITE, RED, second_plus_action,
                                  MAIN_FONT.get_height() // 2 - get_width_text(MAIN_FONT, "+") // 2)
    second_player_minus_b = Button(MAIN_FONT.get_height(), MAIN_FONT.get_height(), "-",
                                   BLACK, WHITE, RED, second_minus_action,
                                   MAIN_FONT.get_height() // 2 - get_width_text(MAIN_FONT, "-") // 2)
    next_player_turn = Button(get_width_text(MAIN_FONT, "Next player turn"), MAIN_FONT.get_height(), "Next player turn",
                              BLACK, WHITE, RED, next_turn_action)

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if not run:
            break

        # Переход хода.
        if CURRENT_TURN == 1:
            first_player_plus_b.freeze = False
            first_player_minus_b.freeze = False
            second_player_plus_b.freeze = True
            second_player_minus_b.freeze = True
        else:
            first_player_plus_b.freeze = True
            first_player_minus_b.freeze = True
            second_player_plus_b.freeze = False
            second_player_minus_b.freeze = False

        # Победа.
        win_text = ""
        if STONES_LEFT == 0 and CURRENT_TURN == 1:
            win_text = "Player 2 wins!"

        if STONES_LEFT == 0 and CURRENT_TURN == 2:
            win_text = "Player 1 wins!"

        if win_text != "":
            draw_win_text(win_text)
            break

        draw_window(first_player_heap, second_player_heap, main_heap,
                    first_player_plus_b, first_player_minus_b,
                    second_player_plus_b, second_player_minus_b,
                    next_player_turn)


# Запуск только при непосредственном обращении к файлу.
if __name__ == "__main__":
    main()
