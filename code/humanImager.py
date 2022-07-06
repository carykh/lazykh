import argparse
import os.path
import pygame
import numpy as np
import math
import shutil
import random
from utils import removeTags, getFilenameOfLine, getTopic, capitalize

def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 40
    for i in range(len(lines)):
        fw, fh = font.size(lines[i])

        # (tx, ty) is the top-left of the font surface
        tx = x - fw / 2
        ty = y + y_offset*i

        font_surface = font.render(lines[i], True, colour)
        screen.blit(font_surface, (tx, ty))



parser = argparse.ArgumentParser(description='blah')
parser.add_argument('--input_file', type=str,  help='the script')
args = parser.parse_args()
INPUT_FILE = args.input_file
B_FOLDER = INPUT_FILE+"_billboards"

f = open(INPUT_FILE+".txt","r+")
lines = list(filter(None, f.read().split("\n"))) # Filter out empty lines, since those won't need drawings.

f.close()

canvassy = None
texty = None
LINE_TIME_LIMIT = 60000
START_DRAW_GAP = -1  # How many milliseconds after a frame change that the drawing is disabled, to prevent accidentally drawing on Image 2 as soon as it flips over. (I disabled this by making it negative.)
LINE_ON = 0
INK_COLOR = None

pygame.init()
screen = pygame.display.set_mode((1400, 1000))
font = pygame.font.SysFont("Helvetica", 36)
canvasFont = pygame.font.SysFont("Jygquif 2", 80)

def getNewInkColor():
    choice = random.random()*3
    if choice < 1.0:
        col = (choice,(1-choice)*0.7,0)
    elif choice < 2.0:
        col = (0,(choice-1)*0.7,1-(choice-1))
    else:
        col = (1-(choice-2),0,(choice-2))
    newCol = (int(col[0]*256),int(col[1]*256),int(col[2]*256))
    return newCol

def refreshCanvas():
    global drawing
    global canvassy
    global INK_COLOR
    canvassy = pygame.surface.Surface((880, 1000))
    canvassy.fill((230,230,230))
    if LINE_ON < len(lines):
        font_surface = canvasFont.render(capitalize(getTopic(lines[LINE_ON])), True, (0,0,0))
        FSW = font_surface.get_size()[0]
        canvassy.blit(font_surface,(440-FSW/2,880))
    INK_COLOR = getNewInkColor()
    drawing = False

def switchLines(first):
    global LINE_ON
    global lastLineSwitchTime
    global texty
    global canvassy
    lastLineSwitchTime = pygame.time.get_ticks()

    if not first: # We don't want to save any images on the very first initialization of the program.
        if not os.path.isdir(B_FOLDER):
            os.mkdir(B_FOLDER)
        pygame.image.save(canvassy, B_FOLDER+"/"+getFilenameOfLine(lines[LINE_ON])+".png")
    while LINE_ON < len(lines) and os.path.exists(B_FOLDER+"/"+getFilenameOfLine(lines[LINE_ON])+".png"): # If you've already drawn that image, skip it and move on to the next one.
        LINE_ON += 1

    texty = pygame.surface.Surface((500, 300))
    texty.fill((100,100,100))
    refreshCanvas()
    if LINE_ON == len(lines):
        renderTextCenteredAt("You're all done.", font, (255,0,0), 250, 50, texty, 460)
    else:
        renderTextCenteredAt(lines[LINE_ON], font, (255,255,255), 250, 50, texty, 460)

switchLines(True)

mouse_loc = (0,0)
prev_mouse_loc = (0,0)
drawing = False
running = True
refreshCanvas()
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                switchLines(False)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.time.get_ticks() >= lastLineSwitchTime+START_DRAW_GAP:
                drawing = True
            mouse_loc = pygame.mouse.get_pos()
            prev_mouse_loc = mouse_loc
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False

    if LINE_ON < len(lines) and pygame.time.get_ticks() >= lastLineSwitchTime+LINE_TIME_LIMIT:
        switchLines(False)
    timeFracLeft = (lastLineSwitchTime+LINE_TIME_LIMIT-pygame.time.get_ticks())/LINE_TIME_LIMIT

    screen.fill((50,50,50))

    if drawing:
        prev_mouse_loc = mouse_loc
        mouse_loc = pygame.mouse.get_pos()
        pygame.draw.line(canvassy,INK_COLOR,prev_mouse_loc,mouse_loc,7)

    screen.blit(canvassy,(0,0))
    screen.blit(texty,(900,20))
    pygame.draw.rect(screen,(0,255,0),(900,320,40,500*timeFracLeft))
    pygame.display.flip()
