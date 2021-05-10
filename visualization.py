import pygame

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("8 Puzzle with A*")

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)

UP = "UP"
LEFT = "LEFT"
RIGHT = "RIGHT"
DOWN = "DOWN"

VIOLET = (148,0,211)
DEEPBLUE = (75,0,130)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
RED = (255,0,0)


class Tile:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

 

def make_grid(rows,width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            tile = Tile(i,j,gap,rows)
            grid[i].append(tile)

    return grid

def draw_grid(win,rows,width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        pygame.draw.line(win,GREY,(i*gap,0),(i*gap,width))
    
def draw(win,grid,rows,width):
    win.fill(WHITE)

    for row in grid:
        for tile in row:
            tile.draw(win)
    
    draw_grid(win,rows,width)
    pygame.display.update()

def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y, x = pos
    
    row = y // gap
    col = x // gap
    return row, col

def move(row,col,grid,direction):

    #print("row=",row,"col=",col)
    if direction == LEFT:
        grid[row][col].color, grid[row-1][col].color = grid[row-1][col].color, grid[row][col].color 
    if direction == RIGHT:
        grid[row][col].color, grid[row+1][col].color = grid[row+1][col].color, grid[row][col].color
    if direction == UP:
        grid[row][col].color, grid[row][col-1].color = grid[row][col-1].color, grid[row][col].color
    if direction == DOWN:
        grid[row][col].color, grid[row][col+1].color = grid[row][col+1].color, grid[row][col].color
    

def get_tile_group(row,col,grid):
    tile_group = []
    for i in range(3):
        for j in range(3):
            tile_group.append(grid[row+i][col+j])
    return tile_group

def make_source_tiles(grid):
    tile_group_colors = [DEEPBLUE,VIOLET,BLUE,GREEN,WHITE,YELLOW,ORANGE,RED,BLACK]
    source_tile_groups = {}
    for i in range(3):
        for j in range(3):
            source_tile_groups[i*3+j] = get_tile_group(3+3*i,3+3*j,grid)
    color_index = -1
    for key,array in source_tile_groups.items():
        color_index +=1
        for tile in array:
            tile.color = tile_group_colors[color_index]
    return source_tile_groups

def make_target_tiles(grid):
    tile_group_colors = [VIOLET,DEEPBLUE,BLUE,GREEN,WHITE,YELLOW,ORANGE,RED,BLACK]
    target_tile_groups = {}
    for i in range(3):
        for j in range(3):
            target_tile_groups[i*3+j] = get_tile_group(38+3*i,3+3*j,grid)
    color_index = -1
    for key,array in target_tile_groups.items():
        color_index +=1
        for tile in array:
            tile.color = tile_group_colors[color_index]
    return target_tile_groups
            
def make_solution_tiles(grid,initial_tiles):
    solution_tile_groups = {}
    for i in range(3):
        for j in range(3):
            solution_tile_groups[i*3+j] = get_tile_group(20+3*i,24+3*j,grid)
    
    for solution_group, initial_group in zip(solution_tile_groups,initial_tiles):
        for solution_tile,initial_tile in zip(solution_tile_groups[solution_group],initial_tiles[initial_group]):
            solution_tile.color = initial_tile.color

    return solution_tile_groups

def main(win,width):
    ROWS = 50
    grid = make_grid(ROWS,width)

    source_tiles = make_source_tiles(grid)
    target_tiles = make_target_tiles(grid)
    solution_tiles = make_solution_tiles(grid,source_tiles)
        

    start = None
    end = None

    run = True

    while run:
        
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos,ROWS,width)
                if row in range(3,12) and col in range(3,12):
                    print("source clicked")
                

            elif pygame.mouse.get_pressed()[2]:
                pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    pass
                if event.key == pygame.K_c:
                    grid = make_grid(ROWS,width)
                    source_tiles = make_source_tiles(grid)
                    target_tiles = make_target_tiles(grid)
                    solution_tiles = make_solution_tiles(grid,source_tiles)

    pygame.quit()
    
main(WIN,WIDTH)
