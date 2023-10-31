import pygame
import random
# Initialize the Pygame font module.
pygame.font.init()
# Set the dimensions of the game window and play area.
s_width = 700
s_height = 700
play_width = 300
play_height = 600
block_size = 30

# Calculate the top-left corner coordinates of the play area.
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height 

# Define Tetris shapes as 2D arrays.
# S, Z, I, O, J, L, and T are defined with dots (.) and zeros (0).

S = [[".....",
      ".....",
      "..00.",
      ".00..",
      "....."],
     [".....",
      "..0..",
      "..00.",
      "...0.",
      "....."]]

Z = [[".....",
      ".....",
      ".00..",
      "..00.",
      "....."],
     [".....",
      "..0..",
      ".00..",
      ".0...",
      "....."]]

I = [["..0..",
      "..0..",
      "..0..",
      "..0..",
      "....."],
     [".....",
      "0000.",
      ".....",
      ".....",
      "....."]]

O = [[".....",
      ".....",
      ".00..",
      ".00..",
      "....."]]

J = [[".....",
      ".0...",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..00.",
      "..0..",
      "..0..",
      "....."],
     [".....",
      ".....",
      ".000.",
      "...0.",
      "....."],
     [".....",
      "..0..",
      "..0..",
      ".00..",
      "....."]]

L = [[".....",
      "...0.",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..0..",
      "..0..",
      "..00.",
      "....."],
     [".....",
      ".....",
      ".000.",
      ".0...",
      "....."],
     [".....",
      ".00..",
      "..0..",
      "..0..",
      "....."]]

T = [[".....",
      "..0..",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..0..",
      "..00.",
      "..0..",
      "....."],
     [".....",
      ".....",
      ".000.",
      "..0..",
      "....."],
     [".....",
      "..0..",
      ".00..",
      "..0..",
      "....."]]

# Create a list of shapes and their corresponding colors.
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(255,105,180),(132,112,255),(139,121,94),(154,205,50),(238,154,0),(142,56,142),(48,128,20)]

# Create a Piece class to represent Tetris pieces.
class Piece(object):

    rows = 20 # Number of rows in the play area
    colums = 10 # Number of columns in the play area
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
        
# Create an empty grid to represent the play area.        
def create_grid(locked_positions = {}):
    grid = [[(0, 0, 0) for x in range(10)] for y in range(20)]   

 # Fill the grid with locked positions and their corresponding colors
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c 
    return grid  

# Define a function to convert the space format of a shape into positions.
def convert_space_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len (shape.shape)]

    for i , line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)  

    return positions   

 
# Check if a shape is in a valid position within the grid.
def valid_space(shape, grid):
    accepted_pos = [(j, i) for i in range(20) for j in range(10) if grid[i][j] == (0, 0, 0)]

    formatted = convert_space_format(shape)

    for pos in formatted:
        x, y = pos
        if x < 0 or x >= 10 or y >= 20:
            return False
        if pos not in accepted_pos:
            if y > -1:
                return False
    return True

# Check if the game is lost.
def check_lost(positions):
    for pos in positions:
        x,y = pos
        if y < 1:
            return True
        
    return False

# Get a random Tetris shape as a Piece.
def get_shape():
    global shapes, shape_colors

    return Piece(5,0, random.choice(shapes))

# Draw text in the middle of the game window.
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("Helvetica", size, bold=True)
    label = font.render(text, 1, color)


    surface.blit(label, (top_left_x + play_width // 2 - label.get_width() // 2, top_left_y + play_height // 2 - label.get_height() // 2))

# Draw the grid lines in the play area.
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines
 

# Clear completed rows and move the blocks above down.
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

# Draw the next shape to be dropped on the side of the play area.
def draw_next_shape(shape,surface):
    font = pygame.font.SysFont('Helvetica', 25)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50 
    sy = top_left_y + play_height/2 - 120

    format = shape.shape[shape.rotation % len(shape.shape)]


    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
               pygame.draw.rect(surface, shape.color, (sx + j*25, sy + i*25, 25, 25), 0)
 

    surface.blit(label, (sx + 10, sy - 45))

# Draw the game window, including the grid and score.
def draw_window(surface, grid, score):
    surface.fill((0,0,0))  

    pygame.font.init()
    font = pygame.font.SysFont('Helvetica',45)
    label = font.render('Tetris',1,(255,255,255))  

    surface.blit(label,(top_left_x + play_width/2 - (label.get_width()/2), 30))

    font = pygame.font.SysFont('Helvetica', 25)
    label = font.render('Score: ' + str(score), 1, (255, 255, 255))


    sx = top_left_x + play_width + 50 
    sy = top_left_y + play_height/2 - 120

    surface.blit(label , (sx + 10,sy + 150))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
    pygame.draw.rect(surface,(0,0,255),(top_left_x,top_left_y,play_width,play_height),4)
    

          
   
    draw_grid(surface, 20, 10)
   



def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.26

    level_time = 0
    score = 0
    back_buffer = pygame.Surface((s_width, s_height))

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()

        if level_time/1000 > 5:# increasing the speed to do game more difficult
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005
        
        clock.tick()

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                  current_piece.x -= 1
                  if not (valid_space(current_piece,grid)):
                      current_piece.x +=1
                if event.key == pygame.K_RIGHT:
                  current_piece.x += 1
                  if not (valid_space(current_piece,grid)):
                      current_piece.x -=1
                if event.key == pygame.K_DOWN:
                  current_piece.y += 1
                  if not (valid_space(current_piece,grid)):
                      current_piece.y -=1
                if event.key == pygame.K_UP:               
                    current_piece.rotation += 1
                    if not (valid_space(current_piece,grid)):
                      current_piece.rotation -=1

        shape_pos = convert_space_format(current_piece)
        
        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > 1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
       # ...

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # Indent the following line properly
            score += clear_rows(grid, locked_positions) * 10

        #win.fill([255,255,255])
        draw_window(back_buffer, grid, score)
        draw_next_shape(next_piece, win)
        
        pygame.display.flip()
        
# ...

        win.blit(back_buffer, (0, 0))
      #  pygame.display.flip()

        if check_lost(locked_positions):
         draw_text_middle(win, "You lost", 50, (255, 255, 255))
         pygame.display.update()  
         pygame.time.delay(1500)
         run = False
         pygame.quit()


    pygame.display.quit() 

 # Initialize the game window and start the main menu.     
def main_menu():
   main(win)

win = pygame.display.set_mode((s_width,s_height))
pygame.display.set_caption('Tetris')  
main_menu()  
