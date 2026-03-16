#!/usr/bin/env python3
"""
Snake Game - A classic snake game with nice UI
Controls: Arrow keys to move, Q to quit, R to restart
"""

import curses
import random
import time

# Game constants
SNAKE_CHAR = '█'
FOOD_CHAR = '●'
WALL_CHAR = '█'
EMPTY_CHAR = ' '

# Colors pairs
COLOR_SNAKE = 1
COLOR_FOOD = 2
COLOR_WALL = 3
COLOR_SCORE = 4
COLOR_BORDER = 5


class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.width = 40
        self.height = 20
        self.score = 0
        self.game_over = False
        self.paused = False
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(COLOR_SNAKE, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_FOOD, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(COLOR_WALL, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_SCORE, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(COLOR_BORDER, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        
        # Hide cursor
        curses.curs_set(0)
        
        # Calculate offset to center the game
        self.offset_x = (curses.COLS - self.width) // 2
        self.offset_y = (curses.LINES - self.height) // 2
        
        self.reset_game()
    
    def reset_game(self):
        """Reset the game state"""
        # Snake starts in the middle, moving right
        self.snake = [
            (self.width // 2, self.height // 2),
            (self.width // 2 - 1, self.height // 2),
            (self.width // 2 - 2, self.height // 2)
        ]
        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.spawn_food()
    
    def spawn_food(self):
        """Spawn food at a random position not occupied by snake"""
        while True:
            self.food = (
                random.randint(1, self.width - 2),
                random.randint(1, self.height - 2)
            )
            if self.food not in self.snake:
                break
    
    def handle_input(self):
        """Handle keyboard input"""
        try:
            key = self.stdscr.getch()
        except:
            return
        
        # Direction keys
        if key == curses.KEY_UP and self.direction != (0, 1):
            self.next_direction = (0, -1)
        elif key == curses.KEY_DOWN and self.direction != (0, -1):
            self.next_direction = (0, 1)
        elif key == curses.KEY_LEFT and self.direction != (1, 0):
            self.next_direction = (-1, 0)
        elif key == curses.KEY_RIGHT and self.direction != (-1, 0):
            self.next_direction = (1, 0)
        # Quit
        elif key in [ord('q'), ord('Q')]:
            self.game_over = True
        # Restart
        elif key in [ord('r'), ord('R')]:
            self.reset_game()
        # Pause
        elif key in [ord('p'), ord('P')]:
            self.paused = not self.paused
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        # Apply direction
        self.direction = self.next_direction
        
        # Calculate new head position
        new_head = (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        )
        
        # Check wall collision
        if (new_head[0] <= 0 or new_head[0] >= self.width - 1 or
            new_head[1] <= 0 or new_head[1] >= self.height - 1):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Move snake
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.spawn_food()
        else:
            self.snake.pop()
    
    def draw_box(self):
        """Draw the game border"""
        # Draw corners and borders
        for x in range(self.width):
            self.stdscr.addch(self.offset_y, self.offset_x + x, WALL_CHAR, 
                            curses.color_pair(COLOR_BORDER) | curses.A_BOLD)
            self.stdscr.addch(self.offset_y + self.height - 1, self.offset_x + x, WALL_CHAR,
                            curses.color_pair(COLOR_BORDER) | curses.A_BOLD)
        
        for y in range(self.height):
            self.stdscr.addch(self.offset_y + y, self.offset_x, WALL_CHAR,
                            curses.color_pair(COLOR_BORDER) | curses.A_BOLD)
            self.stdscr.addch(self.offset_y + y, self.offset_x + self.width - 1, WALL_CHAR,
                            curses.color_pair(COLOR_BORDER) | curses.A_BOLD)
    
    def draw(self):
        """Render the game"""
        self.stdscr.clear()
        
        # Draw title
        title = "🐍 SNAKE 🐍"
        title_x = self.offset_x + (self.width - len(title)) // 2
        self.stdscr.addstr(self.offset_y - 2, title_x, title, 
                          curses.color_pair(COLOR_SCORE) | curses.A_BOLD)
        
        # Draw score
        score_text = f"Score: {self.score}"
        score_x = self.offset_x + (self.width - len(score_text)) // 2
        self.stdscr.addstr(self.offset_y + self.height, score_x, score_text,
                          curses.color_pair(COLOR_SCORE) | curses.A_BOLD)
        
        # Draw game border
        self.draw_box()
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            char = SNAKE_CHAR
            if i == 0:
                char = '▓'  # Head
            color = curses.color_pair(COLOR_SNAKE)
            if i == 0:
                color |= curses.A_BOLD
            self.stdscr.addch(self.offset_y + y, self.offset_x + x, char, color)
        
        # Draw food
        fx, fy = self.food
        self.stdscr.addch(self.offset_y + fy, self.offset_x + fx, FOOD_CHAR,
                         curses.color_pair(COLOR_FOOD) | curses.A_BOLD)
        
        # Draw game over
        if self.game_over:
            game_over_text = "GAME OVER!"
            go_x = self.offset_x + (self.width - len(game_over_text)) // 2
            go_y = self.offset_y + self.height // 2
            self.stdscr.addstr(go_y - 1, go_x, game_over_text, 
                              curses.color_pair(COLOR_FOOD) | curses.A_BOLD | curses.A_BLINK)
            restart_text = "Press R to restart"
            rx = self.offset_x + (self.width - len(restart_text)) // 2
            self.stdscr.addstr(go_y + 1, rx, restart_text,
                              curses.color_pair(COLOR_SCORE))
        
        # Draw paused
        if self.paused and not self.game_over:
            paused_text = "PAUSED"
            px = self.offset_x + (self.width - len(paused_text)) // 2
            py = self.offset_y + self.height // 2
            self.stdscr.addstr(py, px, paused_text,
                              curses.color_pair(COLOR_SCORE) | curses.A_BOLD)
        
        # Draw controls hint
        controls = "Arrow Keys: Move | P: Pause | Q: Quit | R: Restart"
        cx = (curses.COLS - len(controls)) // 2
        self.stdscr.addstr(curses.LINES - 1, cx, controls, 
                          curses.A_DIM)
        
        self.stdscr.refresh()
    
    def run(self):
        """Main game loop"""
        self.draw()
        
        while True:
            self.handle_input()
            self.update()
            self.draw()
            
            if not self.game_over and not self.paused:
                time.sleep(0.1)  # Game speed
            
            if self.game_over:
                time.sleep(0.1)


def main(stdscr):
    """Entry point"""
    game = SnakeGame(stdscr)
    game.run()


if __name__ == "__main__":
    curses.wrapper(main)