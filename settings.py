import pygame as pg
import main
import json

from collections import defaultdict
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

items = defaultdict(list)

def makeFieldWithIncreasements(text, pos, surface, variable, steps):
    myFont = pg.font.SysFont('Press Start 2P', 16)

    textSurface = myFont.render(text, False, (0, 0, 0))
    surface.blit(textSurface, pos)

    textSurface = myFont.render(f' + ', False, (0, 0, 0), (255,255,255))
    surface.blit(textSurface, (pos[0] + 300,pos[1]))

    items[variable].append((pos[0] + 300,pos[1]))

    textSurface = myFont.render(f' - ', False, (0, 0, 0), (255,255,255))
    surface.blit(textSurface, (pos[0] + 380,pos[1]))
    items[variable].append((pos[0] + 380,pos[1]))

    items[variable].append(steps)

def setupSettings(surface: pg.surface.Surface):
    bg = pg.image.load("./image/Sprite-0001.png")
    surface.blit(bg, (0, 0))

    exitIcon = pg.image.load("./image/sand.png")
    surface.blit(exitIcon, (surface.get_width() - 40, 10))


    makeFieldWithIncreasements(f'Hue Value: {hueValue}', (100,140), surface, "hueValue",1)

    makeFieldWithIncreasements(f'Hue steps: {hueSteps}', (100,180), surface, "hueSteps",0.1)

    makeFieldWithIncreasements(f'Hue Limit: {hueLimit}', (100,220), surface, "hueLimit",1)

    makeFieldWithIncreasements(f'Hue Min: {hueMin}', (100,260), surface, "hueMin",1)

    myFont = pg.font.SysFont('Press Start 2P', 16)

    textSurface = myFont.render(" Submit Changes ", False, (51,102,0))
    surface.blit(textSurface, (300, 400))

def setup():
    # initialize and prepare screen
    pg.init()
    surface = pg.display.set_mode((800, 480))


    global hueValue
    global hueSteps
    global hueLimit
    global hueMin

    with open('settings.json', 'r+') as f:
        d = json.load(f)
        hueValue = d["hue_value"]
        hueSteps = d["hue_steps"]
        hueLimit = d["hue_limit"]
        hueMin = d["hue_min"]


    setupSettings(surface)

    
    
    clock = pg.time.Clock()
    done = False
    while not done:
        pg.display.update()
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                main.setup()
                done = 1
                break
            elif e.type == pg.MOUSEBUTTONDOWN:
                x,y = e.pos

                if x > 320 and x < 540 and y > 400 and y < 420:
                    with open('settings.json', 'r+') as f:
                        d = json.load(f)
                        d["hue_value"] = hueValue
                        d["hue_steps"] = hueSteps
                        d["hue_limit"] = hueLimit
                        d["hue_min"] = hueMin
                        f.seek(0)
                        f.write(json.dumps(d))
                        f.truncate()
                    main.setup()
                    done = 1
                    break
                elif x > 760 and x < surface.get_width() and y > 0 and y < 30:
                    main.setup()
                    done = 1
                    break
                else:
                    for key in items:
                        data = items.get(key)
                        plusBtnPos = data[0]
                        MinusBtnPos = data[1]
                        steps = data[2]
                        if x >= plusBtnPos[0] and x <= plusBtnPos[0] + 50 and y >= plusBtnPos[1] - 10 and y <= plusBtnPos[1] + 20:
                            globals()[key] = round(globals()[key] + steps, 1)
                        elif x >= MinusBtnPos[0] and x <= MinusBtnPos[0] + 50 and y >= MinusBtnPos[1] - 10 and y <= MinusBtnPos[1] + 20:
                            globals()[key] = round(globals()[key] - steps, 1)

                    surface.fill(0)
                    items.clear()
                    setupSettings(surface)

        if not done:
            clock.tick(50)
    pg.quit()