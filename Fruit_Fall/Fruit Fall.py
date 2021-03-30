from tkinter import *
from time import *
from random import *

root = Tk()
screen = Canvas(root, width = 1000, height = 1000, background = "#aacbff")
screen.pack()

#============================ Main Menu Screens ============================#
def mainMenu():
    global mainMenuScreen
    
    importImages()
    
    mainMenuScreen = screen.create_image(503, 500, image = mainMenugif)
    screen.bind("<Button-1>", menuMouseHandler)

def menuMouseHandler(event):
    xMouse = event.x
    yMouse = event.y

    # Main menu to select difficulty screen
    if 100 <= xMouse <= 407 and 283 <= yMouse <= 440:
        screen.delete(mainMenuScreen)
        difficulty()

    # Main menu to instructions screen
    elif 100 <= xMouse <= 407 and 513 <= yMouse <= 670:
        screen.delete(mainMenuScreen)
        instructions()

    # Quit game in main menu
    elif 100 <= xMouse <= 407 and 743 <= yMouse <= 900:
        root.destroy()

def instructions():
    global instructionsScreen
    
    instructionsScreen = screen.create_image(502, 502, image = instructionsgif)
    screen.bind("<Button-1>", instructionsMouseHandler)

def instructionsMouseHandler(event):
    xMouse = event.x
    yMouse = event.y

    # Instructions screen back to main menu
    if 49 <= xMouse <= 155 and 49 <= yMouse <= 155:
        screen.delete(instructionsScreen)
        mainMenu()

def difficulty():
    global difficultyScreen

    difficultyScreen = screen.create_image(502, 502, image = difficultygif)
    screen.bind("<Button-1>", difficultyMouseHandler)

def difficultyMouseHandler(event):
    xMouse = event.x
    yMouse = event.y

    # Select difficulty screen back to main menu
    if 49 <= xMouse <= 155 and 49 <= yMouse <= 155:
        screen.delete(difficultyScreen)
        mainMenu()

    # If difficulty is being selected, set mode values and run game
    elif 348 <= xMouse <= 656:
        # Set values for easy mode
        if 135 <= yMouse <= 293:
            setEasyValues()
            
        # Set values for normal mode
        elif 422 <= yMouse <= 580:
            setNormalValues()
            
        # Set values for hard mode
        elif 710 <= yMouse <= 868:
            setHardValues()

        screen.delete(difficultyScreen)
        runGame()

def importImages():
    global backgroundHill, backgroundTree, backgroundScore, backgroundLives
    global basketgif1, basketgif2, lemongif, applegif, cherrygif, peargif, orangegif, lostlifeapple
    global mainMenugif, instructionsgif, difficultygif, gameOvergif
    
    # Importing game background images
    backgroundHill = PhotoImage(file = "hill.gif")
    backgroundTree = PhotoImage(file = "tree.gif")
    backgroundScore = PhotoImage(file = "score.gif")
    backgroundLives = PhotoImage(file = "lives.gif")

    # Importing alternating basket images
    basketgif1 = PhotoImage(file = "basket.gif")
    basketgif2 = PhotoImage(file = "collectingbasket.gif")

    # Importing fruit images
    lemongif = PhotoImage(file = "lemon.gif")
    applegif = PhotoImage(file = "apple.gif")
    cherrygif = PhotoImage(file = "cherry.gif")
    peargif = PhotoImage(file = "pear.gif")
    orangegif = PhotoImage(file = "orange.gif")

    # Importing lives image
    lostlifeapple = PhotoImage(file = "lostlifeapple.gif")

    # Importing screen images
    mainMenugif = PhotoImage(file = "mainmenu.gif")
    instructionsgif = PhotoImage(file = "instructions.gif")
    difficultygif = PhotoImage(file = "difficulty.gif")
    gameOvergif = PhotoImage(file = "gameover.gif")

#============================ Running the Game ============================#
def setEasyValues():
    global wellTimedScore, okTimedScore, gravity, fruitDelay

    # Change scoring system
    wellTimedScore = 25
    okTimedScore = 10

    # Change fruit falling speed
    gravity = 10

    # Change delay between summoning fruit
    fruitDelay = 32

def setNormalValues():
    global wellTimedScore, okTimedScore, gravity, fruitDelay

    wellTimedScore = 100
    okTimedScore = 50
    
    gravity = 20
    
    fruitDelay = 16

def setHardValues():
    global wellTimedScore, okTimedScore, gravity, fruitDelay

    wellTimedScore = 250
    okTimedScore = 100
    
    gravity = 40
    
    fruitDelay = 4

def runGame():
    screen.bind("<Key>", keyDownHandler)
    screen.bind("<KeyRelease>", keyUpHandler)
    screen.bind("<Button-1>", gameMouseHandler)

    # Set initial game values and count down
    setInitialValues()
    countdown()

    # Main game loop running while player still has lives
    while playerAlive == True:
        activateFruit()
        drawObjects()
        updateObjects()
        deleteObjects()
        countLives()

    # Once all lives are lost, delete all images on screen and go to game over screen
    screen.delete(all)
    gameOver()

def countdown():
    # 3 second countdown before beginning the game (gives player time to change from mouse clicking to find game keys)
    for c in range(3,-1,-1):
        if c == 0:
            countdown = screen.create_text(500, 500, text = "Go!", font = "Helvetica 64 bold", fill = "white")
            
        else:
            countdown = screen.create_text(500, 500, text = c, font = "Helvetica 64 bold", fill = "white")
            
        screen.update()
        sleep(1)
        screen.delete(countdown)

def setInitialValues():
    global totalScore, lives, initialFruitY, playerAlive, hKeyPressed, jKeyPressed, kKeyPressed
    global fruit, fruitY, fruitX, fruitImage, basketImage1, basketImage2, basketImage3, basket1Y, basket2Y, basket3Y
    global livesImage1, livesImage2, livesImage3, livesImage4, livesImage5, fruitChoices, lastFewFruit, discardedFruit

    # Game values
    totalScore = 0
    lives = 5
    initialFruitY = 0
    playerAlive = True

    # Fruit arrays
    fruit = []
    fruitY = []
    fruitX = []
    fruitImage = []

    # Basket variables
    basketImage1 = basketgif1
    basketImage2 = basketgif1
    basketImage3 = basketgif1
    
    basket1Y = 750
    basket2Y = 750
    basket3Y = 750

    # Lives images
    livesImage1 = applegif # Reuse the apple GIF for existing lives
    livesImage2 = applegif
    livesImage3 = applegif
    livesImage4 = applegif
    livesImage5 = applegif

    # Fruit selection arrays
    fruitChoices = ["NoFruit"] * 100 + ["apple"] + ["orange"] + ["cherry"] + ["pear"] + ["lemon"] + ["appleorange"] + ["applecherry"] + ["applepear"] + ["applelemon"] + ["orangecherry"] + ["orangepear"] + ["orangelemon"] + ["cherrypear"] + ["cherrylemon"] + ["pearlemon"]
    lastFewFruit = ["NoFruit"] * fruitDelay
    discardedFruit = [] # Array to mix up the types of fruit summoned

    # Keys pressed
    hKeyPressed = False
    jKeyPressed = False
    kKeyPressed = False

def drawObjects():
    global hill, tree, scoreBorder, livesBorder, basket1, basket2, basket3, scoreText
    global livesText, lives1, lives2, lives3, lives4, lives5

    # Draw background
    hill = screen.create_image(500, 500, image = backgroundHill)
    tree = screen.create_image(450, 20, image = backgroundTree)
    scoreBorder = screen.create_image(300, 930, image = backgroundScore)
    livesBorder = screen.create_image(638, 930, image = backgroundLives)
    
    basket1 = screen.create_image(300, basket1Y, image = basketImage1)
    basket2 = screen.create_image(500, basket2Y, image = basketImage2)
    basket3 = screen.create_image(700, basket3Y, image = basketImage3)

    lives1 = screen.create_image(600, 930, image = livesImage1)
    lives2 = screen.create_image(645, 930, image = livesImage2)
    lives3 = screen.create_image(690, 930, image = livesImage3)
    lives4 = screen.create_image(735, 930, image = livesImage4)
    lives5 = screen.create_image(780, 930, image = livesImage5)

    scoreText = screen.create_text(300, 930, text = ("Score: " + str(totalScore)), font = "Helvetica 24 bold", fill = "white")
    livesText = screen.create_text(525, 930, text = "Lives:", font = "Helvetica 24 bold", fill = "white")

    # If fruit is active, draw fruit
    for f in range(len(fruitY) - 1, -1, -1):
        fruit[f] = screen.create_image(fruitX[f], fruitY[f], image = fruitImage[f])

def updateObjects():
    global fruitY

    # Update fallen distance of each active fruit by gravity of selected mode in each frame
    for f in range(len(fruitY) - 1, -1, -1):
        fruitY[f] += gravity

def deleteObjects():
    global lives, fruit, fruitImage, fruitY, fruitX

    # Update, sleep, delete background images
    screen.update()
    sleep(0.03)
    screen.delete(hill, tree, scoreBorder, livesBorder, basket1, basket2, basket3, scoreText, livesText, lives1, lives2, lives3, lives4, lives5)

    # Delete all existing fruit from frame
    for f in range(len(fruitY) - 1, -1, -1):
        screen.delete(fruit[f])

        # If fruit reaches mud, remove fruit values from arrays and player loses a life
        if fruitY[f] > 870:
            fruit.remove(fruit[f])
            fruitImage.remove(fruitImage[f])
            fruitY.remove(fruitY[f])
            fruitX.remove(fruitX[f])
            lives -= 1

def countLives():
    global livesImage1, livesImage2, livesImage3, livesImage4, livesImage5, playerAlive

    # Change life apple images if lives are lost
    if lives == 4:
        livesImage5 = lostlifeapple

    elif lives == 3:
        livesImage5 = lostlifeapple
        livesImage4 = lostlifeapple
    
    elif lives == 2:
        livesImage5 = lostlifeapple
        livesImage4 = lostlifeapple
        livesImage3 = lostlifeapple

    elif lives == 1:
        livesImage5 = lostlifeapple
        livesImage4 = lostlifeapple
        livesImage3 = lostlifeapple
        livesImage2 = lostlifeapple

    # Stop the loop running the game once all lives are lost
    elif lives <= 0:
        playerAlive = False

#============================ Selecting Fruit ============================#
def activateFruit():
    global fruit, fruitImage, fruitX, fruitY
    
    # Fruit selection
    currentFruit = selectFruit()    
    doubleFruitX = doubleFallToBasket() # If summoning a pair of fruit, we need different X values for each to not spawn in same location

    # Summon one fruit at a time and add initial value of fruit to arrays
    if currentFruit == "apple" and "apple" not in fruit:
        appleX = fallToBasket()

        fruit.append("apple")
        fruitImage.append(applegif)
        fruitX.append(appleX)
        fruitY.append(initialFruitY)

    elif currentFruit == "orange" and "orange" not in fruit:
        orangeX = fallToBasket()

        fruit.append("orange")
        fruitImage.append(orangegif)
        fruitX.append(orangeX)
        fruitY.append(initialFruitY)

    elif currentFruit == "lemon" and "lemon" not in fruit:
        lemonX = fallToBasket()

        fruit.append("lemon")
        fruitImage.append(lemongif)
        fruitX.append(lemonX)
        fruitY.append(initialFruitY)

    elif currentFruit == "cherry" and "cherry" not in fruit:
        cherryX = fallToBasket()

        fruit.append("cherry")
        fruitImage.append(cherrygif)
        fruitX.append(cherryX)
        fruitY.append(initialFruitY)

    elif currentFruit == "pear" and "pear" not in fruit:
        pearX = fallToBasket()

        fruit.append("pear")
        fruitImage.append(peargif)
        fruitX.append(pearX)
        fruitY.append(initialFruitY)

    # Summon two fruit at once and add initial values of fruit pairs to arrays
    elif currentFruit == "appleorange" and "appleO" not in fruit and "orangeA" not in fruit:
        appleOX = doubleFruitX[0]
        orangeAX = doubleFruitX[1]

        fruit.append("appleO")
        fruit.append("orangeA")
        fruitImage.append(applegif)
        fruitImage.append(orangegif)
        fruitX.append(appleOX)
        fruitX.append(orangeAX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)

    elif currentFruit == "applecherry" and "appleC" not in fruit and "cherryA" not in fruit:
        appleCX = doubleFruitX[0]
        cherryAX = doubleFruitX[1]
        
        fruit.append("appleC")
        fruit.append("cherryA")
        fruitImage.append(applegif)
        fruitImage.append(cherrygif)
        fruitX.append(appleCX)
        fruitX.append(cherryAX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)

    elif currentFruit == "applepear" and "appleP" not in fruit and "pearA" not in fruit:
        applePX = doubleFruitX[0]
        pearAX = doubleFruitX[1]
        
        fruit.append("appleP")
        fruit.append("pearA")
        fruitImage.append(applegif)
        fruitImage.append(peargif)
        fruitX.append(applePX)
        fruitX.append(pearAX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)

    elif currentFruit == "applelemon" and "appleL" not in fruit and "lemonA" not in fruit:
        appleLX = doubleFruitX[0]
        lemonAX = doubleFruitX[1]
        
        fruit.append("appleL")
        fruit.append("lemonA")
        fruitImage.append(applegif)
        fruitImage.append(lemongif)
        fruitX.append(appleLX)
        fruitX.append(lemonAX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)

    elif currentFruit == "orangecherry" and "orangeC" not in fruit and "cherryO" not in fruit:
        orangeCX = doubleFruitX[0]
        cherryOX = doubleFruitX[1]
        
        fruit.append("orangeC")
        fruit.append("cherryO")
        fruitImage.append(orangegif)
        fruitImage.append(cherrygif)
        fruitX.append(orangeCX)
        fruitX.append(cherryOX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)

    elif currentFruit == "orangepear" and "orangeP" not in fruit and "pearO" not in fruit:
        orangePX = doubleFruitX[0]
        pearOX = doubleFruitX[1]
        
        fruit.append("orangeP")
        fruit.append("pearO")
        fruitImage.append(orangegif)
        fruitImage.append(peargif)
        fruitX.append(orangePX)
        fruitX.append(pearOX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)

    elif currentFruit == "orangelemon" and "orangeL" not in fruit and "lemonO" not in fruit:
        orangeLX = doubleFruitX[0]
        lemonOX = doubleFruitX[1]
        
        fruit.append("orangeL")
        fruit.append("lemonO")
        fruitImage.append(orangegif)
        fruitImage.append(lemongif)
        fruitX.append(orangeLX)
        fruitX.append(lemonOX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)

    elif currentFruit == "cherrypear" and "cherryP" not in fruit and "pearC" not in fruit:
        cherryPX = doubleFruitX[0]
        pearCX = doubleFruitX[1]
        
        fruit.append("cherryP")
        fruit.append("pearC")
        fruitImage.append(cherrygif)
        fruitImage.append(peargif)
        fruitX.append(cherryPX)
        fruitX.append(pearCX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)

    elif currentFruit == "cherrylemon" and "cherryL" not in fruit and "lemonC" not in fruit:
        cherryLX = doubleFruitX[0]
        lemonCX = doubleFruitX[1]
        
        fruit.append("cherryL")
        fruit.append("lemonC")
        fruitImage.append(cherrygif)
        fruitImage.append(lemongif)
        fruitX.append(cherryLX)
        fruitX.append(lemonCX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)

    elif currentFruit == "pearlemon" and "pearL" not in fruit and "lemonP" not in fruit:
        pearLX = doubleFruitX[0]
        lemonPX = doubleFruitX[1]
        
        fruit.append("pearL")
        fruit.append("lemonP")
        fruitImage.append(peargif)
        fruitImage.append(lemongif)
        fruitX.append(pearLX)
        fruitX.append(lemonPX)
        fruitY.append(initialFruitY)
        fruitY.append(initialFruitY)
        
def selectFruit():
    global fruitChoices, lastFewFruit, discardedFruit

    # If fruit delay has passed, possible to summon a fruit/fruit pair
    if lastFewFruit == ["NoFruit"] * fruitDelay:
        selectedFruit = choice(fruitChoices)
        discardedFruit.append(selectedFruit)
        fruitChoices.remove(selectedFruit)
        lastFewFruit.append(selectedFruit)
        lastFewFruit.remove(lastFewFruit[0])

    # If fruit/fruit pair has been summoned recently, wait for fruit delay to pass    
    else:
        selectedFruit = "NoFruit"
        lastFewFruit.append(selectedFruit)
        lastFewFruit.remove(lastFewFruit[0])

    # If fruit selection array is empty, refill the array
    if len(discardedFruit) == 115:
        fruitChoices += discardedFruit
        discardedFruit.clear()

    return selectedFruit

def fallToBasket():
    # Select random basket the fruit will fall to
    basketNum = randint(1, 3)

    if basketNum == 1:
        fruitX = 300

    elif basketNum == 2:
        fruitX = 500

    elif basketNum == 3:
        fruitX = 700

    return fruitX

def doubleFallToBasket():
    # If a fruit pair will be summoned
    basketNumValues = [1, 2, 3]
    basketRemovedValues = []
    fruitXValues = []

    # Select random basket the fruit will fall to
    chosenBasketNum = choice(basketNumValues)

    if chosenBasketNum == 1:
        fruitX = 300

    elif chosenBasketNum == 2:
        fruitX = 500

    elif chosenBasketNum == 3:
        fruitX = 700

    fruitXValues.append(fruitX)
    
    # Make sure the pair of fruit will not fall to the same basket
    basketNumValues.remove(chosenBasketNum)

    # Select random basket from other choices that the other fruit will fall to
    chosenBasketNum2 = choice(basketNumValues)

    if chosenBasketNum2 == 1:
        fruitX = 300

    elif chosenBasketNum2 == 2:
        fruitX = 500

    elif chosenBasketNum2 == 3:
        fruitX = 700

    fruitXValues.append(fruitX)

    return fruitXValues

#============================ Game Key Bindings ============================#
def keyDownHandler(event):
    global keyPressed, hKeyPressed, jKeyPressed, kKeyPressed, basketImage1, basketImage2, basketImage3
    global basket1Y, basket2Y, basket3Y

    # Control the baskets collecting fruit
    keyPressed = event.keysym

    if keyPressed == "h":
        if basket1Y > 730:
            basketImage1 = basketgif2
            basket1Y -= 20

        # Make sure that collecting fruit will not work when the key is held, but only when pressed/tapped 
        if hKeyPressed == False:
            updateScoreH()
            
        hKeyPressed = True
        
    if keyPressed == "j":
        if basket2Y > 730:
            basketImage2 = basketgif2
            basket2Y -= 20
            
        if jKeyPressed == False:
            updateScoreJ()
            
        jKeyPressed = True

    if keyPressed == "k":
        if basket3Y > 730:
            basketImage3 = basketgif2
            basket3Y -= 20
            
        if kKeyPressed == False:
            updateScoreK()
            
        kKeyPressed = True

def keyUpHandler(event):
    global hKeyPressed, jKeyPressed, kKeyPressed, basketImage1, basketImage2, basketImage3, basket1Y, basket2Y, basket3Y

    # Return to original basket position when key is released
    if event.keysym == "h":
        basket1Y = 750
        basketImage1 = basketgif1
        hKeyPressed = False

    if event.keysym == "j":
        basket2Y = 750
        basketImage2 = basketgif1
        jKeyPressed = False

    if event.keysym == "k":
        basket3Y = 750
        basketImage3 = basketgif1
        kKeyPressed = False

def updateScoreH():
    global lives, fruit, fruitImage, fruitX, fruitY, totalScore

    # Update score when fruit comes in contact with left basket
    score = 0

    # Checks if any fruit in array shares X value with basket
    if 300 in fruitX:
        findX = 0
        fruitXIndex = 0

        # Find first fruit in array where its X value matches with the basket
        while findX != 300:
            for f in range(fruitXIndex):
                findX = fruitX[f]

            fruitXIndex += 1

        fruitDistance = 750 - fruitY[fruitXIndex - 2]

        # Update score based on timing of key being pressed
        if fruitDistance > -120 and fruitDistance <= 150:            
            if fruitDistance >= -50 and fruitDistance <= 50:
                score = wellTimedScore
                
            elif fruitDistance >= -70 and fruitDistance <= 100:
                score = okTimedScore

            # Lose a life if timing is poor    
            else:
                lives -= 1

            # Remove fruit values from arrays
            totalScore += score
            screen.delete(fruit[fruitXIndex - 2])
            fruit.remove(fruit[fruitXIndex - 2])
            fruitImage.remove(fruitImage[fruitXIndex - 2])
            fruitX.remove(fruitX[fruitXIndex - 2])
            fruitY.remove(fruitY[fruitXIndex - 2])

def updateScoreJ():
    global lives, fruit, fruitImage, fruitX, fruitY, totalScore

    # Update score when fruit comes in contact with middle basket
    score = 0

    if 500 in fruitX:
        findX = 0
        fruitXIndex = 0

        while findX != 500:
            for f in range(fruitXIndex):
                findX = fruitX[f]

            fruitXIndex += 1

        fruitDistance = 750 - fruitY[fruitXIndex - 2]

        if fruitDistance > -120 and fruitDistance <= 150:           
            if fruitDistance >= -50 and fruitDistance <= 50:
                score = wellTimedScore
                
            elif fruitDistance >= -70 and fruitDistance <= 100:
                score = okTimedScore
                
            else:
                lives -= 1
                
            totalScore += score
            screen.delete(fruit[fruitXIndex - 2])
            fruit.remove(fruit[fruitXIndex - 2])
            fruitImage.remove(fruitImage[fruitXIndex - 2])
            fruitX.remove(fruitX[fruitXIndex - 2])
            fruitY.remove(fruitY[fruitXIndex - 2])

def updateScoreK():
    global lives, fruit, fruitImage, fruitX, fruitY, totalScore

    # Update score when fruit comes in contact with right basket
    score = 0

    if 700 in fruitX:
        findX = 0
        fruitXIndex = 0

        while findX != 700:
            for f in range(fruitXIndex):
                findX = fruitX[f]

            fruitXIndex += 1

        fruitDistance = 750 - fruitY[fruitXIndex - 2]

        if fruitDistance > -120 and fruitDistance <= 150:            
            if fruitDistance >= -50 and fruitDistance <= 50:
                score = wellTimedScore
                
            elif fruitDistance >= -70 and fruitDistance <= 100:
                score = okTimedScore
                
            else:
                lives -= 1
                
            totalScore += score
            screen.delete(fruit[fruitXIndex - 2])
            fruit.remove(fruit[fruitXIndex - 2])
            fruitImage.remove(fruitImage[fruitXIndex - 2])
            fruitX.remove(fruitX[fruitXIndex - 2])
            fruitY.remove(fruitY[fruitXIndex - 2])

def gameMouseHandler(event):
    # Remove binding for mouse clicks in game so other procedures will not trigger
    pass

#============================ Game Over Screen ============================#
def gameOver():
    global gameOverScreen, finalScoreBorder, finalScore

    gameOverScreen = screen.create_image(503, 500, image = gameOvergif)
    finalScoreBorder = screen.create_image(700, 350, image = backgroundLives)
    finalScore = screen.create_text(700, 350, text = ("Final Score: " + str(totalScore)), font = "Helvetica 24 bold", fill = "white")
    
    screen.bind("<Button-1>", endMouseHandler)    

def endMouseHandler(event):
    xMouse = event.x
    yMouse = event.y

    # Game over screen to main menu
    if 100 <= xMouse <= 407 and 283 <= yMouse <= 440:
        screen.delete(gameOverScreen, finalScoreBorder, finalScore)
        mainMenu()

    # Retry on same difficulty from game over screen        
    elif 100 <= xMouse <= 407 and 513 <= yMouse <= 670:
        screen.delete(gameOverScreen, finalScoreBorder, finalScore)
        runGame()

    # Quit game from game over screen
    elif 100 <= xMouse <= 407 and 743 <= yMouse <= 900:
        root.destroy()
        
#============================ Program Procedures ============================#
# Start game from main menu
root.after(0, mainMenu)

# At the bottom
screen.pack()
screen.focus_set()
root.mainloop()
