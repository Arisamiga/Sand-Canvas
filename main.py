import pygame as pg
import math
import random
import colorsys
import settings
import json
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
os.environ['SDL_VIDEO_CENTERED'] = '1'
# -------- Helper functions ---------

def make2DArray(cols, rows):
    arr = [0] * cols
    for i in range(0, len(arr)):
        arr[i] = [0] * rows
    return arr

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))


def withinBounds(i, side):
    return i >= 0 and i <= side-1


w = 20
hueValue = 200
hueSteps = 0.1
hueLimit = 20
hueMin = 12

def defaultConf(d,f):
    d["hue_value"] = 200
    d["hue_steps"] = 0.1
    d["hue_limit"] = 20
    d["hue_min"] = 12
    f.seek(0)
    f.write(json.dumps(d))
    f.truncate()

def setup():
    global hueValue
    global hueSteps
    global hueLimit
    global hueMin
    # initialize and prepare screen
    pg.init()

    surface = pg.display.set_mode((800, 480), pg.FULLSCREEN)
    
    cols = surface.get_width() // w
    rows = surface.get_height() // w

    grid = make2DArray(cols, rows)

    clock = pg.time.Clock()

    with open('settings.json', 'r+') as f:
        d = json.load(f)
        if len(d) < 4:
            defaultConf(d,f)
        else:
            hueValue = d["hue_value"]
            hueSteps = d["hue_steps"]
            hueLimit = d["hue_limit"]
            hueMin = d["hue_min"]
    done = False
    while not done:
        grid = loop(surface, cols, rows, grid)
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                done = 1
                break
            elif e.type == pg.MOUSEBUTTONDOWN:
                if (e.pos[0] < 22 and e.pos[1] < 22):
                    settings.setup()
                    done = 1
                    break
            elif e.type == pg.MOUSEMOTION:
                hueValue = mousePressed(grid, e.pos[0], e.pos[1], cols, rows, hueValue)
        if not done:
            clock.tick(50)
    pg.quit()

def mousePressed(grid,mouseX, mouseY, cols, rows, hueValue):
    mouseCol = math.floor(mouseX / w)
    mouseRow = math.floor(mouseY / w)

    matrix = 2
    extention = math.floor(matrix/2)
    for i in range(-extention, extention):
        for j in range(-extention, extention):
            col = mouseCol + i
            row  = mouseRow + j
            if random.randint(0,1) < 0.75:
                if withinBounds(col, cols) and withinBounds(row, rows):
                    grid[col][row] = hueValue

    newValue = hueValue + hueSteps
    if hueValue >= hueLimit:
        newValue = hueMin

    return newValue

def loop(surface: pg.surface.Surface, cols, rows, grid):
    surface.fill(0)
    for i in range (0, cols):
        for e in range(0, rows):
            if grid[i][e] == 0:
                color = (255, 255, 255)
            else:
                color = hsv2rgb(grid[i][e]/100,0.35,0.63)
            
            x = i * w
            y = e * w
            pg.draw.rect(surface, color, (x,y,w,w))

    nextGrid = make2DArray(cols,rows)
    for i in range (0, cols):
        for e in range(0, rows):
            state = grid[i][e]
            if state > 0:
                # Check that it is not the last row and that there is a bottom row
                # Below
                direc = [-1,1]
                random.shuffle(direc)
                direc = direc[0]

                currentState = grid[i][e]

                lastRow = e < rows - 1
                if lastRow and grid[i][e+1] == 0:
                    nextGrid[i][e+1] = currentState
                
                # Below right
                elif lastRow and withinBounds(i + direc, cols) and grid[i + direc][e + 1] == 0:
                    nextGrid[i + direc][e + 1] = currentState
                
                # Bellow Left
                elif lastRow and withinBounds(i - direc, cols) and grid[i - direc][e + 1] == 0:
                    nextGrid[i - direc][e + 1] = currentState
                else:
                    nextGrid[i][e] = currentState
    setting = pg.image.load("./image/gear.png")
    surface.blit(setting, (2, 2))
    return nextGrid


if __name__ == "__main__":
    setup()
    pg.quit()
    exit(0)
