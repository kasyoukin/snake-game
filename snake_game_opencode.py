#!/usr/bin/env python3
"""
Snake Game - A classic snake game using Python curses library.
Features: Arrow keys control, score display, game over on collision, colorful UI.
"""

import curses
import random
import time


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    sh, sw = stdscr.getmaxyx()

    game_area_top = 2
    game_area_bottom = sh - 2
    game_area_left = 2
    game_area_right = sw - 2

    snake_body = [
        [sh // 2, sw // 2],
        [sh // 2, sw // 2 - 1],
        [sh // 2, sw // 2 - 2]
    ]

    direction = curses.KEY_RIGHT
    pending_direction = direction

    def spawn_food():
        while True:
            food = [
                random.randint(game_area_top, game_area_bottom - 1),
                random.randint(game_area_left, game_area_right - 1)
            ]
            if food not in snake_body:
                return food

    food = spawn_food()
    score = 0
    game_over = False
    paused = False

    def draw_border():
        for x in range(game_area_left - 1, game_area_right + 2):
            stdscr.addch(game_area_top - 1, x, '═', curses.color_pair(5))
            stdscr.addch(game_area_bottom, x, '═', curses.color_pair(5))

        for y in range(game_area_top - 1, game_area_bottom + 1):
            stdscr.addch(y, game_area_left - 1, '║', curses.color_pair(5))
            stdscr.addch(y, game_area_right, '║', curses.color_pair(5))

        stdscr.addch(game_area_top - 1, game_area_left - 1, '╔', curses.color_pair(5))
        stdscr.addch(game_area_top - 1, game_area_right, '╗', curses.color_pair(5))
        stdscr.addch(game_area_bottom, game_area_left - 1, '╚', curses.color_pair(5))
        stdscr.addch(game_area_bottom, game_area_right, '╝', curses.color_pair(5))

    def draw_score():
        score_text = f" Score: {score} "
        stdscr.addstr(0, sw // 2 - len(score_text) // 2, score_text, curses.color_pair(4) | curses.A_BOLD)

    def draw_instructions():
        instructions = " P: Pause | Q: Quit "
        stdscr.addstr(1, sw // 2 - len(instructions) // 2, instructions, curses.color_pair(4))

    def draw_snake():
        head_char = '●'
        if direction == curses.KEY_UP:
            head_char = '▲'
        elif direction == curses.KEY_DOWN:
            head_char = '▼'
        elif direction == curses.KEY_LEFT:
            head_char = '◄'
        elif direction == curses.KEY_RIGHT:
            head_char = '►'

        stdscr.addch(snake_body[0][0], snake_body[0][1], head_char, curses.color_pair(2) | curses.A_BOLD)

        for segment in snake_body[1:]:
            stdscr.addch(segment[0], segment[1], '●', curses.color_pair(1))

    def draw_food():
        stdscr.addch(food[0], food[1], '★', curses.color_pair(3) | curses.A_BOLD)

    def show_game_over():
        game_over_text = " GAME OVER! "
        final_score_text = f" Final Score: {score} "
        restart_text = " Press R to Restart or Q to Quit "

        box_y = sh // 2 - 3
        box_x = sw // 2 - 20

        stdscr.addstr(box_y, box_x, "╔" + "═" * 38 + "╗", curses.color_pair(6))
        for i in range(1, 6):
            stdscr.addstr(box_y + i, box_x, "║" + " " * 38 + "║", curses.color_pair(6))
        stdscr.addstr(box_y + 6, box_x, "╚" + "═" * 38 + "╝", curses.color_pair(6))

        stdscr.addstr(box_y + 2, sw // 2 - len(game_over_text) // 2, game_over_text,
                     curses.color_pair(6) | curses.A_BOLD | curses.A_BLINK)
        stdscr.addstr(box_y + 3, sw // 2 - len(final_score_text) // 2, final_score_text, curses.color_pair(4))
        stdscr.addstr(box_y + 5, sw // 2 - len(restart_text) // 2, restart_text, curses.color_pair(2))

    def show_pause():
        pause_text = " PAUSED "
        resume_text = " Press P to Resume "
        stdscr.addstr(sh // 2, sw // 2 - len(pause_text) // 2, pause_text,
                     curses.color_pair(4) | curses.A_BOLD | curses.A_BLINK)
        stdscr.addstr(sh // 2 + 1, sw // 2 - len(resume_text) // 2, resume_text, curses.color_pair(2))

    while True:
        stdscr.clear()
        draw_border()
        draw_score()
        draw_instructions()

        if game_over:
            show_game_over()
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('r') or key == ord('R'):
                snake_body[:] = [
                    [sh // 2, sw // 2],
                    [sh // 2, sw // 2 - 1],
                    [sh // 2, sw // 2 - 2]
                ]
                direction = curses.KEY_RIGHT
                pending_direction = direction
                food = spawn_food()
                score = 0
                game_over = False
                continue
            elif key == ord('q') or key == ord('Q'):
                break
            time.sleep(0.05)
            continue

        if paused:
            show_pause()
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord('p') or key == ord('P'):
                paused = False
            elif key == ord('q') or key == ord('Q'):
                break
            time.sleep(0.05)
            continue

        key = stdscr.getch()

        if key == ord('q') or key == ord('Q'):
            break

        if key == ord('p') or key == ord('P'):
            paused = True
            continue

        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if (key == curses.KEY_UP and direction != curses.KEY_DOWN) or \
               (key == curses.KEY_DOWN and direction != curses.KEY_UP) or \
               (key == curses.KEY_LEFT and direction != curses.KEY_RIGHT) or \
               (key == curses.KEY_RIGHT and direction != curses.KEY_LEFT):
                pending_direction = key

        direction = pending_direction

        new_head = snake_body[0].copy()
        if direction == curses.KEY_UP:
            new_head[0] -= 1
        elif direction == curses.KEY_DOWN:
            new_head[0] += 1
        elif direction == curses.KEY_LEFT:
            new_head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            new_head[1] += 1

        if (new_head[0] < game_area_top or new_head[0] >= game_area_bottom or
            new_head[1] < game_area_left or new_head[1] >= game_area_right):
            game_over = True
            continue

        if new_head in snake_body:
            game_over = True
            continue

        snake_body.insert(0, new_head)

        if new_head == food:
            score += 10
            food = spawn_food()
            speed = max(50, 100 - score // 2)
            stdscr.timeout(speed)
        else:
            snake_body.pop()

        draw_snake()
        draw_food()
        stdscr.refresh()
        time.sleep(0.01)


def run_game():
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run_game()
