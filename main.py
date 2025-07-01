import pygame as pg

def make2DArray(cols, rows):
    arr = [None] * cols
    for i in range(0, len(arr)):
        arr[i] = [None] * rows
    return arr


w = 10


def setup():
    # initialize and prepare screen
    pg.init()

    surface = pg.display.set_mode((400, 400))
    cols = surface.get_width() // w
    rows = surface.get_height() // w

    grid = make2DArray(cols, rows)

    for i in range (0, cols):
        for e in range(0, rows):
            grid[i][e] = 0

    clock = pg.time.Clock()

    grid[20][10] = 1
    done = False
    while not done:
        loop(surface, cols, rows, grid)
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
        clock.tick(50)
    pg.quit()

def loop(surface: pg.surface.Surface, cols, rows, grid):
    surface.fill(0)
    for i in range (0, cols):
        for e in range(0, rows):
            color = pg.color.Color(grid[i][e] * 255, grid[i][e] * 255, grid[i][e] * 255)
            colorBorder = pg.color.Color(255,255,255)
            x = i * w
            y = e * w
            pg.draw.rect(surface, colorBorder, (x,y,w,w))
            pg.draw.rect(surface, color, (x,y,w-1,w-1))




if __name__ == "__main__":
    setup()
    pg.quit()
