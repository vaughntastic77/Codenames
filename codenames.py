#----------------------------------------------------------------------------------------------------------------------
# Codenames board game written in python by Jacob Vaughn 12/30/2025
#----------------------------------------------------------------------------------------------------------------------
import pygame as pg
import random
import numpy as np

# Initialize Pygame
pg.init()

# Set the size of the window
winSize = (1720,1040)
screen = pg.display.set_mode((winSize[0],winSize[1]))
pg.display.set_caption("Codenames")

# Create clock for timing
clock = pg.time.Clock()
FPS = 60

# Background Color
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (150,150,150)
screen.fill(BLACK) 

# Initialize fonts
titleFont = pg.font.SysFont("Arial",48,bold=True)
menuFont = pg.font.SysFont("Arial",36)
gameFont = pg.font.SysFont("Arial",24)
wordsFont = pg.font.SysFont("Arial",36,bold=True)

# Load board image
board = pg.transform.scale(pg.image.load("images/board.png"),winSize)

# Read all words into a list, only once
with open('wordlist.txt', 'r') as f:
    wordlist = [line.strip() for line in f if line.strip()]

words = random.sample(wordlist,25)

#----------------------------------------------------------------------------------------------------------------------
# Draw all images on screen in current position
#----------------------------------------------------------------------------------------------------------------------
def draw(opts):
    # Draw board
    screen.fill(BLACK) 
    screen.blit(board,(0,0))
    # Display each marble at current position
    # for c in range(0,4):
        # for m in range(0,4):
            # screen.blit(marbs[c],pos[c,m]) 
    # Waiting to roll text
    if opts == 1:
        # textTurn = gameFont.render(colors[turn]+"'s turn.",True,WHITE)
        # screen.blit(textTurn,(winSize//2 - textTurn.get_width()//2,710))
        textRoll = gameFont.render("Press Space to roll.",True,WHITE)
        screen.blit(textRoll,(winSize[0]//2 - textRoll.get_width()//2,740))
    # Choosing marble text
    elif opts == 2:
        textMarb = gameFont.render("Choose which to move.",True,WHITE)
        screen.blit(textMarb,(winSize[0]//2 - textMarb.get_width()//2,725))
    # Choosing move text
    elif opts == 3:
        textMove1 = gameFont.render("Choose where to move",True,WHITE)
        screen.blit(textMove1,(winSize[0]//2 - textMove1.get_width()//2,710))
        textMove2 = gameFont.render("or press Esc to go back.",True,WHITE)
        screen.blit(textMove2,(winSize[0]//2 - textMove2.get_width()//2,740))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)


#----------------------------------------------------------------------------------------------------------------------
# Show main menu and wait for selection
#----------------------------------------------------------------------------------------------------------------------
def menu():
    draw(0)
    # Draw menu background
    menuSize = 400
    pg.draw.rect(screen,(200,200,200),pg.Rect(winSize[0]//2 - menuSize//2,winSize[1]//2 - menuSize//2,menuSize,menuSize))
    # Draw menu text
    title = titleFont.render("Codenames",True,BLACK)
    screen.blit(title,(winSize[0]//2 - title.get_width()//2,winSize[1]//2 - title.get_height()//2 - 130))
    text1 = menuFont.render("[R] Resume Last Game",True,BLACK)
    screen.blit(text1,(winSize[0]//2 - text1.get_width()//2,winSize[1]//2 - text1.get_height()//2 - 50))
    text2 = menuFont.render("[N] New Game",True,BLACK)
    screen.blit(text2,(winSize[0]//2 - text2.get_width()//2,winSize[1]//2 - text2.get_height()//2 - 0))
    textE = menuFont.render("[Esc] Exit",True,BLACK)
    screen.blit(textE,(winSize[0]//2 - textE.get_width()//2,winSize[1]//2 - textE.get_height()//2 + 150))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)
    # Choose menu option
    while True:
        for event in pg.event.get():
            # Close window
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # Key pressed
            elif event.type == pg.KEYDOWN:
                # Load game
                if event.key == pg.K_r:
                    return
                    # return loadGame()
                # New game
                elif event.key == pg.K_n:
                    return newMenu()
                # Quit (ESC)
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

#----------------------------------------------------------------------------------------------------------------------
# Show new game menu and wait for selection
#----------------------------------------------------------------------------------------------------------------------
def newMenu():
    global nPlayers, computers
    draw(0)
    # Draw menu background
    menuSize = 400
    pg.draw.rect(screen,(200,200,200),pg.Rect(winSize[0]//2 - menuSize//2,winSize[1]//2 - menuSize//2,menuSize,menuSize))
    # Draw menu text
    title = titleFont.render("Codenames",True,BLACK)
    screen.blit(title,(winSize[0]//2 - title.get_width()//2,winSize[1]//2 - title.get_height()//2 - 130))
    text1 = menuFont.render("[1] One Player",True,BLACK)
    screen.blit(text1,(winSize[0]//2 - text1.get_width()//2,winSize[1]//2 - text1.get_height()//2 - 50))
    text2 = menuFont.render("[2] Two Players",True,BLACK)
    screen.blit(text2,(winSize[0]//2 - text2.get_width()//2,winSize[1]//2 - text2.get_height()//2 - 0))
    text3 = menuFont.render("[3] Three Players",True,BLACK)
    screen.blit(text3,(winSize[0]//2 - text3.get_width()//2,winSize[1]//2 - text3.get_height()//2 + 50))
    text4 = menuFont.render("[4] Four Players",True,BLACK)
    screen.blit(text4,(winSize[0]//2 - text4.get_width()//2,winSize[1]//2 - text4.get_height()//2 + 100))
    textE = menuFont.render("[Esc] Back",True,BLACK)
    screen.blit(textE,(winSize[0]//2 - textE.get_width()//2,winSize[1]//2 - textE.get_height()//2 + 150))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)
    # Reinitialize positions
    # newGame()
    # Choose menu option
    while True:
        for event in pg.event.get():
            # Close window
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # Key pressed
            elif event.type == pg.KEYDOWN:
                # One Player
                if event.key == pg.K_1:
                    nPlayers = 1
                    return
                # Two Player
                elif event.key == pg.K_2:
                    nPlayers = 2
                    return
                # Three Player
                elif event.key == pg.K_3:
                    nPlayers = 3
                    return
                # Four Player
                elif event.key == pg.K_4:
                    nPlayers = 4
                    return
                # No Players
                elif event.key == pg.K_0:
                    nPlayers = 0
                    computers = True
                    return
                # Back to main menu (ESC)
                elif event.key == pg.K_ESCAPE:
                    return menu()


#----------------------------------------------------------------------------------------------------------------------
# Pause menu
#----------------------------------------------------------------------------------------------------------------------
def pause():
    draw(0)
    # Draw menu background
    menuSize = 350
    pg.draw.rect(screen,(200,200,200),pg.Rect(winSize[0]//2 - menuSize//2,winSize[1]//2 - menuSize//2,menuSize,menuSize))
    # Draw menu text
    title = titleFont.render("Codenames",True,BLACK)
    screen.blit(title,(winSize[0]//2 - title.get_width()//2,winSize[1]//2 - title.get_height()//2 - 100))
    text1 = menuFont.render("[R] Resume Game",True,BLACK)
    screen.blit(text1,(winSize[0]//2 - text1.get_width()//2,winSize[1]//2 - text1.get_height()//2 - 0))
    text2 = menuFont.render("[S] Save and Quit",True,BLACK)
    screen.blit(text2,(winSize[0]//2 - text2.get_width()//2,winSize[1]//2 - text2.get_height()//2 + 50))
    textE = menuFont.render("[Esc] Quit to Menu",True,BLACK)
    screen.blit(textE,(winSize[0]//2 - textE.get_width()//2,winSize[1]//2 - textE.get_height()//2 + 100))
    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)
    # Choose menu option
    while True:
        for event in pg.event.get():
            # Close window
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # Key pressed
            elif event.type == pg.KEYDOWN:
                # Resume game
                if event.key == pg.K_r:
                    return True
                # Save and quit game
                elif event.key == pg.K_s:
                    # saveGame()
                    return False
                # Quit to main menu (ESC)
                elif event.key == pg.K_ESCAPE:
                    return False


#----------------------------------------------------------------------------------------------------------------------
# Main game loop
#----------------------------------------------------------------------------------------------------------------------
def main():
    global turn
    running = True
    while running:
        menu()
        # In game loop
        inGame = True
        while inGame:
            # Events
            for event in pg.event.get():
                # Close window
                if event.type == pg.QUIT:
                    inGame = False
                    running = False
                # Key pressed
                elif event.type == pg.KEYDOWN:
                    # Roll die (return)
                    if event.key == pg.K_SPACE:
                        inGame = True
                    elif event.key == pg.K_p:
                        inGame = pause()

            # Display game
            draw(1)
            clock.tick(FPS)

    # Close pygame
    pg.quit()

main()
