import time
from solver import solve_sudoku, is_valid_entry
import pygame
pygame.font.init()

icon = pygame.image.load("header.jpg")

pygame.display.set_icon(icon)


class Cube:
    ROWS = 9
    COLS = 9

    def __init__(self, val, row, col, width ,height):
        self.val = val
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.is_selected = False

    def draw(self, window):
        fnt = pygame.font.SysFont("comicsans", 40)

        distance = self.width / 9
        x = self.col * distance
        y = self.row * distance

        if self.temp != 0 and self.val == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            window.blit(text, (x+5, y+5))
        elif not(self.val == 0):
            text = fnt.render(str(self.val), 1, (0, 0, 0))
            window.blit(text, (x + (distance/2 - text.get_width()/2), y + (distance/2 - text.get_height()/2)))

        if self.is_selected:
            pygame.draw.rect(window, (255,0,0), (x,y, distance ,distance), 3)

    def set(self, val):
        self.val = val

    def set_temp(self, val):
        self.temp = val



class Grid:


    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, ROWS, COLS, width, height):
        self.ROWS = ROWS
        self.COLS = COLS
        self.box = [[Cube(self.board[i][j], i, j, width, height) for j in range(COLS)] for i in range(ROWS)]
        self.width = width
        self.height = height
        self.model = None
        self.is_selected = None

    def update_model(self):
        self.model = [[self.box[i][j].val for j in range(self.COLS)] for i in range(self.ROWS)]

    def place(self, val):
        row, col = self.is_selected
        if self.box[row][col].val == 0:
            self.box[row][col].set(val)
            self.update_model()

            if is_valid_entry(self.model, val, (row,col)) and solve_sudoku(self.model):
                return True
            else:
                self.box[row][col].set(0)
                self.box[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.is_selected
        self.box[row][col].set_temp(val)

    def draw(self, window):
        # Draw Grid Lines
        distance = self.width / 9
        for i in range(self.ROWS+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(window, (0,0,0), (0, i*distance), (self.width, i*distance), thick)
            pygame.draw.line(window, (0, 0, 0), (i * distance, 0), (i * distance, self.height), thick)

        # Draw Cubes
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.box[i][j].draw(window)

    def select(self, row, col):
        # Reset all other
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self.box[i][j].is_selected = False

        self.box[row][col].is_selected = True
        self.is_selected = (row, col)

    def clear(self):
        row, col = self.is_selected
        if self.box[row][col].val == 0:
            self.box[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            distance = self.width / 9
            x = pos[0] // distance
            y = pos[1] // distance
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.box[i][j].val == 0:
                    return False
        return True



def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

def redraw_window(window, board, time, strikes):
    window.fill((255,255,255))
    fnt = pygame.font.SysFont("comicsans", 40)
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    window.blit(text, (20, 560))
    # Draw time
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    window.blit(text, (540 - 160, 560))
    # Draw grid and board
    board.draw(window)




def main():
    window = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    # pygame.display.set_icon(surface)

    board = Grid(9, 9, 540, 540)
    key = None
    play = True
    start = time.time()
    strikes = 0
    while play:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.is_selected
                    if board.box[i][j].temp != 0:
                        if board.place(board.box[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            play = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.is_selected and key != None:
            board.sketch(key)

        redraw_window(window, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()