import pyscreenshot as ImageGrab
import cv2
import numpy as np


def screenshot():
    im = np.array(ImageGrab.grab())
    # cv2.imwrite('screenshot.jpg', im)
    return im


def findscreen():
    found = False
    print('Finding game screen...')
    while not found:
        # screenshot()
        SS = screenshot()  # cv2.imread('screenshot.jpg', 0)
        SS = cv2.cvtColor(SS, cv2.COLOR_BGR2GRAY)
        ret, TSS = cv2.threshold(SS, 20, 255, cv2.THRESH_BINARY)
        #        cv2.imwrite('BTScreen.jpg', TSS)
        #        cv2.imshow('image', SS)
        #        cv2.waitKey(0)
        #        cv2.destroyAllWindows()
        H, W = 0, 0
        while H < len(TSS) - 600 and not found:
            W = 0
            while W < len(TSS[0]) - 550 and not found:
                if TSS[H][W] < 10:
                    i = 0
                    found = True
                    while found and i < 550:
                        if TSS[H][W + i] > 200:
                            found = False
                        if TSS[H + 599][W + i] > 200:
                            found = False
                        i += 1
                    i = 0
                    while found and i < 600:
                        if TSS[H + i][W] > 200:
                            found = False
                        if TSS[H + i][W + 549] > 200:
                            found = False
                        i += 1
                W += 1
            H += 1
        W -= 1
        H -= 1
        # cv2.imwrite('BTScreen.jpg', TSS)
        if not found:
            print('Please open the game!')
        else:
            print('Game found')
    return H, W


def screenconfirm(H, W):
    # checks if the Width and Height is correct and game is in area we are looking at
    screen = screenshot()
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    ret, screen = cv2.threshold(screen, 20, 255, cv2.THRESH_BINARY)
    if screen[H][W] == 0 and screen[H + 599][W] == 0 and screen[H][W + 549] == 0 and screen[H + 599][W + 549] == 0:
        return True
    else:
        return False


def readsceen():
    screen1 = np.array(ImageGrab.grab())
    screen2 = np.array(ImageGrab.grab())
    screen3 = np.array(ImageGrab.grab())
    screen4 = np.array(ImageGrab.grab())
    screen5 = np.array(ImageGrab.grab())
#    cv2.imwrite('screen1.jpg', screen1)
#    cv2.imwrite('screen2.jpg', screen2)
#    cv2.imwrite('screen3.jpg', screen3)
#    cv2.imwrite('screen4.jpg', screen4)
#    cv2.imwrite('screen5.jpg', screen5)
    return screen1, screen2, screen3, screen4, screen5


def cropgame(SH, SW, SS):
    gamescreen = SS[SH:SH + 600, SW:SW + 550]
    return gamescreen


def findlivesandscore(gamescreen):
    # gamescreen = cv2.cvtColor(gamescreen, cv2.COLOR_BGR2GRAY)
    score = gamescreen[16:45, 130:145]
    # cv2.imwrite('score.jpg',score)
    # lives = gamescreen[61:90, 120:135]
    # cv2.imwrite('lives.jpg', lives)
    SU = score[1][3]
    SM = score[14][3]
    SD = score[27][3]
    SLU = score[6][1]
    SLD = score[20][1]
    SRU = score[6][14]
    SRD = score[20][14]
    # we represent our integers with 7 pixels each showing the state of the line it is in
    # for example SU represents the Upper line in the font so if for example we have all
    # of the above pixels > 200 it means our integer consists of all the lines which means it's 8
    if SM < 200 and SU > 200 and SD > 200 and SLU > 200 and SLD > 200 and SRU > 200 and SRD > 200:
        scoree = 0
    elif SM < 200 and SU < 200 and SD < 200 and SLU > 200 and SLD > 200 and SRU < 200 and SRD < 200:
        scoree = 1
    elif SM > 200 and SU > 200 and SD > 200 and SLU < 200 and SLD > 200 and SRU > 200 and SRD < 200:
        scoree = 2
    elif SM > 200 and SU > 200 and SD > 200 and SLU < 200 and SLD < 200 and SRU > 200 and SRD > 200:
        scoree = 3
    elif SM > 200 and SU < 200 and SD < 200 and SLU > 200 and SLD < 200 and SRU > 200 and SRD > 200:
        scoree = 4
    elif SM > 200 and SU > 200 and SD > 200 and SLU > 200 and SLD < 200 and SRU < 200 and SRD > 200:
        scoree = 5
    elif SM > 200 and SU > 200 and SD > 200 and SLU > 200 and SLD > 200 and SRU < 200 and SRD > 200:
        scoree = 6
    elif SM < 200 and SU > 200 and SD < 200 and SLU < 200 and SLD < 200 and SRU > 200 and SRD > 200:
        scoree = 7
    elif SM > 200 and SU > 200 and SD > 200 and SLU > 200 and SLD > 200 and SRU > 200 and SRD > 200:
        scoree = 8
    elif SM > 200 and SU > 200 and SD > 200 and SLU > 200 and SLD < 200 and SRU > 200 and SRD > 200:
        scoree = 9
    else:
        scoree = 1
    if gamescreen[69][134] > 200:
        life = 2
    else:
        life = 1
    return scoree, life


def finddistance(game):
    # finds the distance between paddle and the ball
    # gamee = game[100:580, :]
    # cv2.imwrite('game.jpg', gamee)
    paddle = game[580:585,:]
    underpaddle = game[585:600,:]
    bally = 100
    ballx = 0
    if sum(sum(underpaddle)) < 10:
        while game[bally][ballx] < 10 and bally < 580:
            ballx = 0
            while game[bally][ballx] < 10 and ballx < 545:
                ballx += 1
            bally += 1
    else:
        bally = 286
        while game[bally][ballx] < 10 and bally < 600:
            ballx = 0
            while game[bally][ballx] < 10 and ballx < 545:
                ballx += 1
            bally += 1
    ballx += 5
    # balls width is 10 pixels so we add 5 to x in order to find its centers y coordinate
    paddlex = 0
    while paddle[1][paddlex] < 10 and paddlex < 549:
        paddlex += 1
    paddlex += 25
    # paddles width is 50 pixels so we add 25 to x in order to find its centers y coordinate
    return int(abs(ballx - paddlex) + abs(bally - 580))


def fitness(distance):  # fitness for each individual until it finds the right movement to catch the ball
    return (1 - distance/996) * 100  # max distance possible between ball and paddle is 996


def main(GSH, GSW):  # GSH : Game Start Hight, GSW : Game Start Width
    # SS = screenshot()
    # SS = cv2.cvtColor(SS, cv2.COLOR_BGR2GRAY)
    # GameScreen = cropgame(GSH, GSW, SS)
    # cv2.imwrite('game' + str(i) + '.jpg', GameScreen)
    screen1, screen2, screen3, screen4, screen5 = readsceen()
    game1 = cropgame(GSH, GSW, screen1)
    game2 = cropgame(GSH, GSW, screen2)
    game3 = cropgame(GSH, GSW, screen3)
    game4 = cropgame(GSH, GSW, screen4)
    game5 = cropgame(GSH, GSW, screen5)
    game1 = cv2.cvtColor(game1, cv2.COLOR_BGR2GRAY)
    game2 = cv2.cvtColor(game2, cv2.COLOR_BGR2GRAY)
    game3 = cv2.cvtColor(game3, cv2.COLOR_BGR2GRAY)
    game4 = cv2.cvtColor(game4, cv2.COLOR_BGR2GRAY)
    game5 = cv2.cvtColor(game5, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite('game1.jpg', game1)
    #cv2.imwrite('game2.jpg', game2)
    #cv2.imwrite('game3.jpg', game3)
    #cv2.imwrite('game4.jpg', game4)
    #cv2.imwrite('game5.jpg', game5)
    score1, life1 = findlivesandscore(game1)
    score2, life2 = findlivesandscore(game2)
    score3, life3 = findlivesandscore(game3)
    score4, life4 = findlivesandscore(game4)
    score5, life5 = findlivesandscore(game5)

    fit = -1
    lifeloss = False
    ballfound = False
    if life1 != life5 and life1 == life4:
        lifeloss = True
        distance = finddistance(game4)
        fit = fitness(distance)
    elif life1 != life5 and life1 == life3:
        lifeloss = True
        distance = finddistance(game3)
        fit = fitness(distance)
    elif life1 != life5 and life1 == life2:
        lifeloss = True
        distance = finddistance(game2)
        fit = fitness(distance)
    elif life1 != life5:
        lifeloss = True
        distance = finddistance(game1)
        fit = fitness(distance)
    elif life1 == life2 and life2 == life3 and life3 == life4 and life4 == life5:
        ballfound = True
        fit = 100
    else:
        fit = -1
    if score5 > score1:
        scoregained = True
        scoreloss = False
    elif score5 < score1:
        scoregained = False
        scoreloss = True
    else:
        scoregained = False
        scoreloss = False
    return fit, lifeloss, ballfound, score5, scoregained, scoreloss
