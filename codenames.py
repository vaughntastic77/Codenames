#----------------------------------------------------------------------------------------------------------------------
# Codenames board game written in python by Jacob Vaughn 12/31/2025
#----------------------------------------------------------------------------------------------------------------------
import pygame as pg
import random
import numpy as np
import os.path
import time
import webbrowser

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
GREY = (210,210,210)
DARKGREY = (100,100,100)
BLUE = (0,0,255)
RED = (255,0,0)
screen.fill(BLACK) 

# Initialize fonts
titleFont = pg.font.SysFont("Arial",48,bold=True)
menuFont = pg.font.SysFont("Arial",36)
gameFont = pg.font.SysFont("Arial",48)
wordFont = pg.font.SysFont("Arial",36,bold=True)
scoreFont = pg.font.SysFont("Arial",60,bold=True)

# Load board image
board = pg.transform.scale(pg.image.load("assets/images/board.png"),winSize)

# Load images
cardSize = (5*61,3*60)
cardImg = pg.transform.scale(pg.image.load("assets/images/word-card.png"),cardSize)
cardSelectImg = pg.transform.scale(pg.image.load("assets/images/word-card-select.png"),cardSize)
cardRedImg = pg.transform.scale(pg.image.load("assets/images/word-card-red.png"),cardSize)
cardBlueImg = pg.transform.scale(pg.image.load("assets/images/word-card-blue.png"),cardSize)
cardBlackImg = pg.transform.scale(pg.image.load("assets/images/word-card-black.png"),cardSize)
redImg1 = pg.transform.scale(pg.image.load("assets/images/red1.png"),cardSize)
redImg2 = pg.transform.scale(pg.image.load("assets/images/red2.png"),cardSize)
redImg3 = pg.transform.scale(pg.image.load("assets/images/red1.png"),cardSize)
redImg4 = pg.transform.scale(pg.image.load("assets/images/red2.png"),cardSize)
redImgs = [redImg1,redImg2,redImg3,redImg4]
blueImg1 = pg.transform.scale(pg.image.load("assets/images/blue1.png"),cardSize)
blueImg2 = pg.transform.scale(pg.image.load("assets/images/blue2.png"),cardSize)
blueImg3 = pg.transform.scale(pg.image.load("assets/images/blue1.png"),cardSize)
blueImg4 = pg.transform.scale(pg.image.load("assets/images/blue2.png"),cardSize)
blueImgs = [blueImg1,blueImg2,blueImg3,blueImg4]
bystImg1 = pg.transform.scale(pg.image.load("assets/images/byst1.png"),cardSize)
bystImg2 = pg.transform.scale(pg.image.load("assets/images/byst2.png"),cardSize)
bystImg3 = pg.transform.scale(pg.image.load("assets/images/byst1.png"),cardSize)
bystImg4 = pg.transform.scale(pg.image.load("assets/images/byst2.png"),cardSize)
bystImgs = [bystImg1,bystImg2,bystImg3,bystImg4]
assnImg = pg.transform.scale(pg.image.load("assets/images/assassin.png"),cardSize)
rndNum = random.randrange(0,4)

redOn = pg.transform.scale(pg.image.load("assets/images/redOn.png"),(80,80))
redOff = pg.transform.scale(pg.image.load("assets/images/redOff.png"),(80,80))
blueOn = pg.transform.scale(pg.image.load("assets/images/blueOn.png"),(80,80))
blueOff = pg.transform.scale(pg.image.load("assets/images/blueOff.png"),(80,80))

# Read all words into a list, only once
with open('assets/wordlist.txt', 'r') as f:
    wordlist = [line.strip() for line in f if line.strip()]

words = np.array(random.sample(wordlist,25))

#----------------------------------------------------------------------------------------------------------------------
# Inialize constants and variables
#----------------------------------------------------------------------------------------------------------------------
# Team colors
teamColors = ["Red","Blue"]
# Settings
if os.path.isfile("settings_Codenames.npy"):
    setVals = np.load("settings_Codenames.npy")
    timeLim = setVals[0]
    numAssns = setVals[1]
    imgStyle = setVals[2]
else:
    timeLim = 60 # Time limit of each turn in seconds
    numAssns = 1 # Number of assassins
    imgStyle = 0 # WIP
imgStyles = ["Classic","WIP"]

# Card numbers
cardNums = np.array(list(range(0,25)))

# Card positions (top left corners)
cardSpacing = 10
cardPos = [[0]*2]*25
i = 0
for r in range(-2,3):
    for c in range(-2,3):
        cardPos[i] = [winSize[0]//2 - cardSize[0]//2 + r*(cardSize[0]+cardSpacing),winSize[1]//2 - cardSize[1]//2 + c*(cardSize[1]+cardSpacing) + 35]
        i += 1

def generateMap():
    global rbFirst, colorCards, assnCards, bystCards, turn, score
    # Randomize starting team: [red,blue]
    rbFirst = random.randrange(0,2)
    # Randomize color cards
    if rbFirst:
        redCards = random.sample(list(cardNums),8)
        blueCards = random.sample(list(set(cardNums)-set(redCards)),9)
    else:
        redCards = random.sample(list(cardNums),9)
        blueCards = random.sample(list(set(cardNums)-set(redCards)),8)
    colorCards = np.array([redCards,blueCards],dtype=object)
    assnCards = np.array(random.sample(list(set(cardNums)-set(redCards)-set(blueCards)),numAssns))
    bystCards = np.array(list(set(cardNums)-set(redCards)-set(blueCards)-set(assnCards)))

    #Initialize game parameters
    turn = rbFirst # [red, blue]
    score = np.array([len(redCards), len(blueCards)]) # Number of [red, blue] cards remaining

generateMap()

# Initialize game parameters
guessing = 0 # [clue,guess]
guessLeft = 0 # Number of guesses left
cardsSelected = np.array([False]*25) # Boolean array of cards that have been selected/revealed


#----------------------------------------------------------------------------------------------------------------------
# Draw all images on screen with various options
#----------------------------------------------------------------------------------------------------------------------
def draw(headerText,opts):
    # Draw board
    screen.fill(BLACK) 
    screen.blit(board,(0,0))
    # Header bar
    pg.draw.rect(screen,GREY,pg.Rect(0,0,1720,75))
    pg.draw.rect(screen,RED,pg.Rect(0,0,winSize[0]//2,5))
    pg.draw.rect(screen,RED,pg.Rect(0,0,5,75))
    pg.draw.rect(screen,RED,pg.Rect(0,75,winSize[0]//2,5))
    pg.draw.rect(screen,BLUE,pg.Rect(winSize[0]//2,0,winSize[0]//2,5))
    pg.draw.rect(screen,BLUE,pg.Rect(1720,0,5,75))
    pg.draw.rect(screen,BLUE,pg.Rect(winSize[0]//2,75,winSize[0]//2,5))
    # Display card grid
    for i in range(0,25):
        screen.blit(cardImg,cardPos[i]) 
        wordText = wordFont.render(words[i],True,BLACK)
        screen.blit(wordText,(cardPos[i][0] + cardSize[0]//2 - wordText.get_width()//2,cardPos[i][1] + 110))
    # Display current score (cards left)
    textScore1 = scoreFont.render(str(score[0]),True,RED)
    screen.blit(textScore1,(90,6))
    textScore2 = scoreFont.render(str(score[1]),True,BLUE)
    screen.blit(textScore2,(1600,6))
    # Display current turn LEDs
    if turn:
        screen.blit(redOff,(0,0))
        screen.blit(blueOn,(1640,0))
    else:
        screen.blit(redOn,(0,0))
        screen.blit(blueOff,(1640,0))

    # Display card grid with map
    if opts == 0:
        for i in range(0,25):
            if i in colorCards[0]:
                screen.blit(cardRedImg,cardPos[i]) 
            elif i in colorCards[1]:
                screen.blit(cardBlueImg,cardPos[i]) 
            elif i in assnCards:
                screen.blit(cardBlackImg,cardPos[i]) 
            else:
                screen.blit(cardImg,cardPos[i]) 
            wordText = wordFont.render(words[i],True,BLACK)
            screen.blit(wordText,(cardPos[i][0] + cardSize[0]//2 - wordText.get_width()//2,cardPos[i][1] + 110))

    # Display selected cards
    elif opts == 1:
        for x in cardNums[cardsSelected]:
            if x in colorCards[0]:
                screen.blit(redImgs[(rndNum+colorCards[0].index(x))%4],cardPos[x])
            elif x in colorCards[1]:
                screen.blit(blueImgs[(rndNum+colorCards[1].index(x))%4],cardPos[x])
            elif x in assnCards:
                screen.blit(assnImg,cardPos[x])
            else:
                screen.blit(bystImgs[(rndNum+list(bystCards).index(x))%4],cardPos[x])

    textHeader = gameFont.render(headerText,True,BLACK)
    screen.blit(textHeader,(winSize[0]//2 - textHeader.get_width()//2,15))

    # Update screen
    pg.event.pump()
    pg.display.update()
    clock.tick(FPS)

#----------------------------------------------------------------------------------------------------------------------
# Write data to savedGame.npz
#----------------------------------------------------------------------------------------------------------------------
def saveGame():
    np.savez("savedGame_Codenames.npz",words=words, rbFirst=rbFirst, colorCards=colorCards, assnCards=assnCards, bystCards=bystCards, turn=turn, guessing=guessing, guessLeft=guessLeft, score=score, cardsSelected=cardsSelected)

#----------------------------------------------------------------------------------------------------------------------
# Load data from savedGame.npz
#----------------------------------------------------------------------------------------------------------------------
def loadGame():
    global words, rbFirst, colorCards, assnCards, bystCards, turn, guessing, guessLeft, score, cardsSelected
    fLoaded = np.load("savedGame_Codenames.npz",allow_pickle=True)

    words = fLoaded["words"]
    rbFirst = fLoaded["rbFirst"]
    colorCards = fLoaded["colorCards"]
    assnCards = fLoaded["assnCards"]
    bystCards = fLoaded["bystCards"]
    turn = fLoaded["turn"]
    guessing = fLoaded["guessing"]
    guessLeft = fLoaded["guessLeft"]
    score = fLoaded["score"]
    cardsSelected = fLoaded["cardsSelected"]

#----------------------------------------------------------------------------------------------------------------------
# Reinitialize positions
#----------------------------------------------------------------------------------------------------------------------
def newGame():
    global words, turn, guessing, guessLeft, score, cardsSelected
    # Words for card grid
    words = np.array(random.sample(list(set(wordlist)-set(words)),25))

    generateMap()

    # Initialize game parameters
    guessing = 0 # [clue,guess]
    guessLeft = 0 # Number of guesses left
    cardsSelected = np.array([False]*25) # Boolean array of cards that have been selected/revealed

    chooseMap()

#----------------------------------------------------------------------------------------------------------------------
# Generate maps until one is chosen and confirmed
#----------------------------------------------------------------------------------------------------------------------
def chooseMap():
    # Draw instructions
    textGen = "Press SPACE to generate new maps. Press ENTER to continue."
    draw(textGen,0)
    # Choose map
    while True:
        # Key pressed
        for event in pg.event.get():
            # Close window
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # Key pressed
            elif event.type == pg.KEYDOWN:
                # Generate new map
                if event.key == pg.K_SPACE:
                    # Draw instructions
                    generateMap()
                    draw(textGen,0)
                # Confrim chosen map
                elif event.key == pg.K_RETURN:
                    # Picture instructions
                    draw("Take a picture of the screen, then press ENTER to begin the game.",0)
                    while True:
                        for ev in pg.event.get():
                            if ev.type == pg.KEYDOWN:
                                if ev.key == pg.K_RETURN:
                                    return

#----------------------------------------------------------------------------------------------------------------------
# Draw menu background with given dimensions
#----------------------------------------------------------------------------------------------------------------------
def drawMenuBG(menuSize):
    pg.draw.rect(screen,GREY,pg.Rect(winSize[0]//2 - menuSize[0]//2,winSize[1]//2 - menuSize[1]//2,menuSize[0],menuSize[1]))
    pg.draw.rect(screen,BLUE,pg.Rect(winSize[0]//2 - menuSize[0]//2,winSize[1]//2 - menuSize[1]//2,menuSize[0]//2,5))
    pg.draw.rect(screen,BLUE,pg.Rect(winSize[0]//2 - menuSize[0]//2,winSize[1]//2 - menuSize[1]//2,5,menuSize[1]))
    pg.draw.rect(screen,BLUE,pg.Rect(winSize[0]//2 - menuSize[0]//2,winSize[1]//2 + menuSize[1]//2,menuSize[0]//2,5))
    pg.draw.rect(screen,RED,pg.Rect(winSize[0]//2,winSize[1]//2 - menuSize[1]//2,menuSize[0]//2,5))
    pg.draw.rect(screen,RED,pg.Rect(winSize[0]//2 + menuSize[0]//2,winSize[1]//2 - menuSize[1]//2,5,menuSize[1]))
    pg.draw.rect(screen,RED,pg.Rect(winSize[0]//2,winSize[1]//2 + menuSize[1]//2,menuSize[0]//2,5))

#----------------------------------------------------------------------------------------------------------------------
# Show main menu and wait for selection
#----------------------------------------------------------------------------------------------------------------------
def menu():
    # Draw menu background
    drawMenuBG((500,400))
    # Draw menu text
    title = titleFont.render("Codenames",True,BLACK)
    screen.blit(title,(winSize[0]//2 - title.get_width()//2,winSize[1]//2 - title.get_height()//2 - 130))
    text1 = menuFont.render("[R] Resume Last Game",True,BLACK)
    screen.blit(text1,(winSize[0]//2 - text1.get_width()//2,winSize[1]//2 - text1.get_height()//2 - 70))
    text2 = menuFont.render("[N] New Game",True,BLACK)
    screen.blit(text2,(winSize[0]//2 - text2.get_width()//2,winSize[1]//2 - text2.get_height()//2 - 20))
    text3 = menuFont.render("[S] Settings",True,BLACK)
    screen.blit(text3,(winSize[0]//2 - text3.get_width()//2,winSize[1]//2 - text3.get_height()//2 + 30))
    text4 = menuFont.render("[H] How to Play",True,BLACK)
    screen.blit(text4,(winSize[0]//2 - text4.get_width()//2,winSize[1]//2 - text4.get_height()//2 + 80))
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
                    return loadGame()
                # New game
                elif event.key == pg.K_n:
                    return newGame()
                # Settings menu
                elif event.key == pg.K_s:
                    return settingsMenu()
                # Open game rules
                elif event.key == pg.K_h:
                    webbrowser.open("https://filemanager.czechgames.com/storage/files/codenames/rules/codenames-rules-en.pdf")
                # Quit (ESC)
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()

#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------
# Show settings menu and wait for selection
def settingsMenu():
    # Draw menu background
    drawMenuBG((500,400))
    # Draw menu text
    title = titleFont.render("Settings",True,BLACK)
    screen.blit(title,(winSize[0]//2 - title.get_width()//2,winSize[1]//2 - title.get_height()//2 - 130))
    text1 = menuFont.render("[T] Time Limit: "+str(timeLim),True,BLACK)
    screen.blit(text1,(winSize[0]//2 - text1.get_width()//2,winSize[1]//2 - text1.get_height()//2 - 40))
    text2 = menuFont.render("[N] Number of Assassins: "+str(numAssns),True,BLACK)
    screen.blit(text2,(winSize[0]//2 - text2.get_width()//2,winSize[1]//2 - text2.get_height()//2 + 10))
    text3 = menuFont.render("[S] Style: "+imgStyles[imgStyle],True,BLACK)
    screen.blit(text3,(winSize[0]//2 - text3.get_width()//2,winSize[1]//2 - text3.get_height()//2 + 60))
    textE = menuFont.render("[Esc] Back",True,BLACK)
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
                # Timer
                if event.key == pg.K_t:
                    return setTimeLim()
                # New game
                elif event.key == pg.K_n:
                    return setNumAssns()
                # Settings menu
                elif event.key == pg.K_s:
                    return setStyle()
                # Quit (ESC)
                elif event.key == pg.K_ESCAPE:
                    np.save("settings_Codenames.npy",np.array([timeLim,numAssns,imgStyle]))
                    return menu()


#----------------------------------------------------------------------------------------------------------------------
# Pause menu
#----------------------------------------------------------------------------------------------------------------------
def setTimeLim():
    return

#----------------------------------------------------------------------------------------------------------------------
# Pause menu
#----------------------------------------------------------------------------------------------------------------------
def setNumAssns():
    return

#----------------------------------------------------------------------------------------------------------------------
# Pause menu
#----------------------------------------------------------------------------------------------------------------------
def setStyle():
    return

#----------------------------------------------------------------------------------------------------------------------
# Pause menu
#----------------------------------------------------------------------------------------------------------------------
def pause():
    # Draw menu background
    drawMenuBG((500,400))
    # Draw menu text
    title = titleFont.render("Codenames",True,BLACK)
    screen.blit(title,(winSize[0]//2 - title.get_width()//2,winSize[1]//2 - title.get_height()//2 - 100))
    text1 = menuFont.render("[R] Resume Game",True,BLACK)
    screen.blit(text1,(winSize[0]//2 - text1.get_width()//2,winSize[1]//2 - text1.get_height()//2 - 20))
    text2 = menuFont.render("[S] Save and Quit",True,BLACK)
    screen.blit(text2,(winSize[0]//2 - text2.get_width()//2,winSize[1]//2 - text2.get_height()//2 + 30))
    text3 = menuFont.render("[H] How to Play",True,BLACK)
    screen.blit(text3,(winSize[0]//2 - text3.get_width()//2,winSize[1]//2 - text3.get_height()//2 + 80))
    textE = menuFont.render("[Esc] Quit to Menu",True,BLACK)
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
                # Resume game
                if event.key == pg.K_r:
                    return True
                # Open game rules
                elif event.key == pg.K_h:
                    webbrowser.open("https://filemanager.czechgames.com/storage/files/codenames/rules/codenames-rules-en.pdf")
                # Save and quit game
                elif event.key == pg.K_s:
                    saveGame()
                    return False
                # Quit to main menu (ESC)
                elif event.key == pg.K_ESCAPE:
                    return False


#----------------------------------------------------------------------------------------------------------------------
# Main game loop
#----------------------------------------------------------------------------------------------------------------------
def main():
    global words, rbFirst, colorCards, assnCards, bystCards, turn, guessing, guessLeft, score, cardsSelected
    running = True
    while running:
        draw("",0)
        menu()
        # In game loop
        inGame = True
        gameOver = False
        winner = -1
        clickTime = 0
        while inGame:
            if guessing:
                # Display game
                if guessLeft == 0:
                    draw("Double-click a card to guess. Guesses remaining: FREE ([P] Pass)",1)
                else:
                    draw("Double-click a card to guess. Guesses remaining: "+str(guessLeft)+" ([P] Pass)",1)
                # Get mouse position
                mousePos = pg.mouse.get_pos()
                # Events
                for event in pg.event.get():
                    # Close window
                    if event.type == pg.QUIT:
                        inGame = False
                        running = False
                    # Key pressed
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_p:
                            guessing = 0
                            guessLeft = 0
                            turn = int(not turn)
                        # Pause menu
                        if event.key == pg.K_ESCAPE:
                            inGame = pause()
                    # Mouse clicked
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        if time.time() - clickTime < 0.5:

                            for i in range(0,25):
                                if cardPos[i][0] <= mousePos[0] <= cardPos[i][0]+cardSize[0] and cardPos[i][1] <= mousePos[1] <= cardPos[i][1]+cardSize[1] and not cardsSelected[i]:
                                    cardsSelected[i] = True
                                    if i in colorCards[turn]:
                                        guessLeft -= 1
                                        score[turn] -= 1
                                    elif i in colorCards[int(not turn)]:
                                        score[int(not turn)] -= 1
                                        guessing = 0
                                        guessLeft = 0
                                        turn = int(not turn)
                                    elif i in assnCards:
                                        gameOver = True
                                    else:
                                        guessing = 0
                                        guessLeft = 0
                                        turn = int(not turn)

                                    # Check for winner
                                    if score[0] == 0:
                                        winner = 0
                                    elif score[1] == 0:
                                        winner = 1
                                    elif gameOver:
                                        winner = int(not turn)
                                    
                                    # Declare winner
                                    if winner != -1:
                                        draw("",1)
                                        # Draw menu background
                                        drawMenuBG((540,300))
                                        # Draw menu text
                                        winnerColor = [RED,BLUE]
                                        title = titleFont.render(teamColors[winner]+" wins!",True,winnerColor[winner])
                                        screen.blit(title,(winSize[0]//2 - title.get_width()//2,winSize[1]//2 - title.get_height()//2 - 50))
                                        text1 = menuFont.render("Press ENTER to quit to Menu",True,BLACK)
                                        screen.blit(text1,(winSize[0]//2 - text1.get_width()//2,winSize[1]//2 - text1.get_height()//2 + 50))
                                        # Update screen
                                        pg.event.pump()
                                        pg.display.update()
                                        clock.tick(FPS)
                                        # Choose menu option
                                        while inGame:
                                            for event in pg.event.get():
                                                # Close window
                                                if event.type == pg.QUIT:
                                                    pg.quit()
                                                    quit()
                                                # Key pressed
                                                elif event.type == pg.KEYDOWN:
                                                    # Back to menu
                                                    if event.key == pg.K_RETURN:
                                                        inGame = False

                            clickTime = 0
                        else:
                            clickTime = time.time()
                # Check if out of guesses
                if guessLeft == -1:
                    guessing = 0
                    guessLeft = 0
                    turn = int(not turn)

            else:
                # Display game
                draw("Say a one-word clue, and type a number: "+str(guessLeft)+"  (ENTER to continue)",1)
                # Events
                for event in pg.event.get():
                    # Close window
                    if event.type == pg.QUIT:
                        inGame = False
                        running = False
                    # Key pressed
                    elif event.type == pg.KEYDOWN:
                        if event.unicode in ['0','1','2','3','4','5','6','7','8','9']:
                            guessLeft = int(event.unicode)
                        elif event.key == pg.K_RETURN:
                            if guessLeft == 0:
                                guessLeft = score[turn]
                            guessing = 1
                        # Pause menu
                        elif event.key == pg.K_ESCAPE:
                            inGame = pause()

            clock.tick(FPS)

    # Close pygame
    pg.quit()

main()
