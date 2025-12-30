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
GREY = (200,200,200)
BLUE = (0,0,255)
RED = (255,0,0)
screen.fill(BLACK) 

# Initialize fonts
titleFont = pg.font.SysFont("Arial",48,bold=True)
menuFont = pg.font.SysFont("Arial",36)
gameFont = pg.font.SysFont("Arial",24)
wordFont = pg.font.SysFont("Arial",36,bold=True)
scoreFont = pg.font.SysFont("Arial",60,bold=True)

# Load board image
board = pg.transform.scale(pg.image.load("images/board.png"),winSize)

# Load images
cardSize = (5*61,3*60)
cardImg = pg.transform.scale(pg.image.load("images/word-card.png"),cardSize)
cardSelectImg = pg.transform.scale(pg.image.load("images/word-card-select.png"),cardSize)
cardRedImg = pg.transform.scale(pg.image.load("images/word-card-red.png"),cardSize)
cardBlueImg = pg.transform.scale(pg.image.load("images/word-card-blue.png"),cardSize)
cardBlackImg = pg.transform.scale(pg.image.load("images/word-card-black.png"),cardSize)
redImg1 = pg.transform.scale(pg.image.load("images/red1.png"),cardSize)
redImg2 = pg.transform.scale(pg.image.load("images/red2.png"),cardSize)
redImg3 = pg.transform.scale(pg.image.load("images/red1.png"),cardSize)
redImg4 = pg.transform.scale(pg.image.load("images/red2.png"),cardSize)
redImgs = [redImg1,redImg2,redImg3,redImg4]
blueImg1 = pg.transform.scale(pg.image.load("images/blue1.png"),cardSize)
blueImg2 = pg.transform.scale(pg.image.load("images/blue2.png"),cardSize)
blueImg3 = pg.transform.scale(pg.image.load("images/blue1.png"),cardSize)
blueImg4 = pg.transform.scale(pg.image.load("images/blue2.png"),cardSize)
blueImgs = [blueImg1,blueImg2,blueImg3,blueImg4]
bystImg1 = pg.transform.scale(pg.image.load("images/byst1.png"),cardSize)
bystImg2 = pg.transform.scale(pg.image.load("images/byst2.png"),cardSize)
bystImg3 = pg.transform.scale(pg.image.load("images/byst1.png"),cardSize)
bystImg4 = pg.transform.scale(pg.image.load("images/byst2.png"),cardSize)
bystImgs = [bystImg1,bystImg2,bystImg3,bystImg4]
assnImg = pg.transform.scale(pg.image.load("images/assassin.png"),cardSize)

# Read all words into a list, only once
with open('wordlist-test.txt', 'r') as f:
    wordlist = [line.strip() for line in f if line.strip()]

words = random.sample(wordlist,25)

#----------------------------------------------------------------------------------------------------------------------
# Inialize constants and variables
#----------------------------------------------------------------------------------------------------------------------
# Settings
numAssns = 1 # Number of assassins
turnTime = 300 # Time limit of each turn in seconds
# imgStyle = 0 # WIP

# Card numbers
cardNums = list(range(0,25))

# Card positions (top left corners)
cardSpacing = 10
cardPos = [[0]*2]*25
i = 0
for r in range(-2,3):
    for c in range(-2,3):
        cardPos[i] = [winSize[0]//2 - cardSize[0]//2 + r*(cardSize[0]+cardSpacing),winSize[1]//2 - cardSize[1]//2 + c*(cardSize[1]+cardSpacing) + 35]
        i = i + 1

rbFirst = random.randrange(0,2)
if rbFirst:
    redCards = np.array(random.sample(cardNums,8))
    blueCards = np.array(random.sample(list(set(cardNums)-set(redCards)),9))
else:
    redCards = np.array(random.sample(cardNums,9))
    blueCards = np.array(random.sample(list(set(cardNums)-set(redCards)),8))

assnCard = np.array(random.sample(list((set(cardNums)-set(redCards))-set(blueCards)),numAssns))
#----------------------------------------------------------------------------------------------------------------------
# Draw all images on screen with various options
#----------------------------------------------------------------------------------------------------------------------
def draw(opts):
    # Draw board
    screen.fill(BLACK) 
    screen.blit(board,(0,0))
    # Display card grid
    for i in range(0,25):
        if i in redCards:
            screen.blit(cardRedImg,cardPos[i]) 
        elif i in blueCards:
            screen.blit(cardBlueImg,cardPos[i]) 
        elif i in assnCard:
            screen.blit(cardBlackImg,cardPos[i]) 
        else:
            screen.blit(cardImg,cardPos[i]) 
        wordText = wordFont.render(words[i],True,BLACK)
        screen.blit(wordText,(cardPos[i][0] + cardSize[0]//2 - wordText.get_width()//2,cardPos[i][1] + 110))
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
    pg.draw.rect(screen,GREY,pg.Rect(winSize[0]//2 - menuSize//2,winSize[1]//2 - menuSize//2,menuSize,menuSize))
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                return newMenu()


#----------------------------------------------------------------------------------------------------------------------
# Show new game menu and wait for selection
#----------------------------------------------------------------------------------------------------------------------
def newMenu():
    global nPlayers, computers
    draw(0)
    # Draw menu background
    menuSize = 400
    pg.draw.rect(screen,GREY,pg.Rect(winSize[0]//2 - menuSize//2,winSize[1]//2 - menuSize//2,menuSize,menuSize))
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                return menu()


#----------------------------------------------------------------------------------------------------------------------
# Pause menu
#----------------------------------------------------------------------------------------------------------------------
def pause():
    draw(0)
    # Draw menu background
    menuSize = 350
    pg.draw.rect(screen,GREY,pg.Rect(winSize[0]//2 - menuSize//2,winSize[1]//2 - menuSize//2,menuSize,menuSize))
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
