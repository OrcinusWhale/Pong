import pygame
import random
import sys
import ctypes
from pygame.locals import *


# Returns whether the ball has hit any of the players
def hit():
    if (0 <= ballPos[0] <= player1.get_width() and player1Pos <= ballPos[1] + ball.get_height() / 2 <= player1Pos + player1.get_height()) or (screen.get_width() >= ballPos[0] + ball.get_width() >= screen.get_width() - player2.get_width() and player2Pos <= ballPos[1] + ball.get_height() / 2 <= player2Pos + player2.get_height()):
        return True
    return False


pygame.init()
# Screen creation
ctypes.windll.user32.SetProcessDPIAware()
true_res = [ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)]
screen = pygame.display.set_mode(true_res, pygame.FULLSCREEN)
# Screen creation
player1 = pygame.image.load('player1.png').convert_alpha()  # First player's image
player2 = pygame.image.load('player2.png').convert_alpha()  # Second player's image
ball = pygame.image.load('ball1.png').convert_alpha()  # Ball's image
pygame.display.set_caption("PONG")  # Changes the window's title to "PONG"
textFont = pygame.font.SysFont('Impact', 200)  # The font for the title
buttonFont = pygame.font.SysFont('impact', 50)  # The font for the buttons
# Text
title = textFont.render("PONG", False, [255, 255, 255])
redWins = textFont.render("RED WINS", False, [255, 0, 0])
blueWins = textFont.render("BLUE WINS", False, [0, 0, 255])
pausedText = textFont.render("PAUSED", False, [255, 255, 255])
playButton = buttonFont.render("Play", False, [255, 255, 255])
resumeButton = buttonFont.render("Resume", False, [255, 255, 255])
resetButton = buttonFont.render("Reset", False, [150, 150, 150])
quitButton = buttonFont.render("Quit", False, [150, 150, 150])
# Text
score1 = 0  # The first player's score
score2 = 0  # The second player's score
highlighted = "play"  # The highlighted button
winScreen = False  # someone won
playing = False  # If the game is currently running
reset = True  # If the game should be reset
first = True  # If the game just booted up
while 1:
    for event in pygame.event.get():  # For every event in the queue
        if event.type == QUIT or pygame.key.get_pressed()[K_LALT] and pygame.key.get_pressed()[K_F4]:  # If quit or alt+f4
            sys.exit()
        elif event.type == KEYDOWN:  # If pressed
            if event.key == K_DOWN:  # Down key
                if highlighted == "play":  # Play button is highlighted
                    highlighted = "quit"
                    playButton = buttonFont.render("Play", False, [150, 150, 150])
                    quitButton = buttonFont.render("Quit", False, [255, 255, 255])
                elif highlighted == "resume":  # Resume button is highlighted
                    highlighted = "reset"
                    resumeButton = buttonFont.render("Resume", False, [150, 150, 150])
                    resetButton = buttonFont.render("Reset", False, [255, 255, 255])
                elif highlighted == "reset":  # Reset button is highlighted
                    highlighted = "quit"
                    resetButton = buttonFont.render("Reset", False, [150, 150, 150])
                    quitButton = buttonFont.render("Quit", False, [255, 255, 255])
            elif event.key == K_UP:  # Up key
                if highlighted == "quit":  # Quit button is highlighted
                    if first:  # If just booted up
                        highlighted = "play"
                        playButton = buttonFont.render("Play", False, [255, 255, 255])
                        quitButton = buttonFont.render("Quit", False, [150, 150, 150])
                    else:
                        highlighted = "reset"
                        quitButton = buttonFont.render("Quit", False, [150, 150, 150])
                        resetButton = buttonFont.render("Reset", False, [255, 255, 255])
                elif highlighted == "reset":  # Reset button is highlighted
                    highlighted = "resume"
                    resumeButton = buttonFont.render("Resume", False, [255, 255, 255])
                    resetButton = buttonFont.render("Reset", False, [150, 150, 150])
            elif event.key == K_RETURN:  # If enter
                if highlighted == "play":  # Play button is highlighted
                    highlighted = "resume"
                    first = False
                    playing = True
                elif highlighted == "resume":  # Resume button is highlighted
                    playing = True
                elif highlighted == "reset":  # Reset button is highlighted
                    score1 = 0
                    score2 = 0
                    playing = True
                    reset = True
                elif highlighted == "quit":  # Quit button is highlighted
                    sys.exit()
    while playing:  # The game is on
        if reset:  # Just booted up or reset
            player1Pos = screen.get_height() / 2 - player1.get_height() / 2  # The first player's position
            player2Pos = screen.get_height() / 2 - player2.get_height() / 2  # The second player's position
            ballPos = [screen.get_width() / 2 - ball.get_width() / 2, screen.get_height() / 2 + ball.get_height() / 2]  # The ball's position
            ballMove = [random.choice([screen.get_width() / 375, -(screen.get_width() / 375)]), random.choice([screen.get_height() / 250, -(screen.get_height() / 250)])]  # The ball's speed
            reset = False
            paused = True  # If the game should be frozen
        if paused:
            screen.fill([0, 0, 0])
            screen.blit(player1, [0, player1Pos])
            screen.blit(player2, [screen.get_width() - player2.get_width(), player2Pos])
            screen.blit(ball, ballPos)
            score1surface = textFont.render(str(score1), False, [255, 255, 255])  # The first player's score text
            screen.blit(score1surface, [screen.get_width() / 4 - score1surface.get_width() / 2, 0])
            score2surface = textFont.render(str(score2), False, [255, 255, 255])  # The second player's score text
            screen.blit(score2surface, [screen.get_width() * 3 / 4 - score2surface.get_width() / 2, 0])
            pygame.display.update()
        while paused and playing:  # The game is on but frozen
            for event in pygame.event.get():  # For every event in queue
                if event.type == QUIT or pygame.key.get_pressed()[K_LALT] and pygame.key.get_pressed()[K_F4]:  # If quit or alt+f4
                    sys.exit()
                elif event.type == KEYDOWN:  # If pressed
                    if event.key == K_SPACE:  # If space
                        paused = False
                    elif event.key == K_ESCAPE:  # If escape
                        playing = False
        if playing:  # If the game is on
            screen.fill([0, 0, 0])
            for event in pygame.event.get():  # For every event in queue
                if event.type == QUIT or pygame.key.get_pressed()[K_LALT] and pygame.key.get_pressed()[K_F4]:  # If quit or alt+f4
                    sys.exit()
                elif event.type == KEYDOWN:  # If pressed
                    if event.key == K_ESCAPE:  # If escape
                        playing = False
            if pygame.key.get_pressed()[K_w] and player1Pos > 0:  # 'W' is pressed and player is not out of bounds
                player1Pos = player1Pos - screen.get_height() / 250
            if pygame.key.get_pressed()[K_s] and player1Pos < screen.get_height() - player1.get_height():  # 'S' is pressed and player is not out of bounds
                player1Pos = player1Pos + screen.get_height() / 250
            if pygame.key.get_pressed()[K_UP] and player2Pos > 0:  # UP is pressed and player is not out of bounds
                player2Pos = player2Pos - screen.get_height() / 250
            if pygame.key.get_pressed()[K_DOWN] and player2Pos < screen.get_height() - player2.get_height():  # DOWN is pressed and player is not out of bounds
                player2Pos = player2Pos + screen.get_height() / 250
            if hit():  # If ball collides with player
                ballMove[0] = -ballMove[0]
            ballPos[0] = ballPos[0] + ballMove[0]
            if 0 < ballPos[1] < screen.get_height() - ball.get_height():  # If ball doesn't collide with ceiling or floor
                ballPos[1] = ballPos[1] + ballMove[1]
            else:
                ballMove[1] = -ballMove[1]
                ballPos[1] = ballPos[1] + ballMove[1]
            screen.blit(player1, [0, player1Pos])
            screen.blit(player2, [screen.get_width() - player2.get_width(), player2Pos])
            screen.blit(score1surface, [screen.get_width() / 4 - score1surface.get_width() / 2, 0])
            screen.blit(score2surface, [screen.get_width() * 3 / 4 - score2surface.get_width() / 2, 0])
            screen.blit(ball, ballPos)
            pygame.display.update()
            if ballPos[0] + ball.get_width() <= 0:  # If second player scored
                score2 += 1
                reset = True
            elif ballPos[0] >= screen.get_width():  # If first player scored
                score1 += 1
                reset = True
            if score1 == 11:  # first player reached 11 points
                highlighted = "play"
                first = True
                playing = False
                reset = True
                score1 = 0
                score2 = 0
                screen.fill([0, 0, 0])
                screen.blit(redWins, [screen.get_width()/2 - redWins.get_width()/2, screen.get_height()/2 - redWins.get_height()/2])
                pygame.display.update()
                winScreen = True
            if score2 == 11:  # second player reached 11 points
                highlighted = "play"
                first = True
                playing = False
                reset = True
                score1 = 0
                score2 = 0
                screen.fill([0, 0, 0])
                screen.blit(blueWins, [screen.get_width() / 2 - blueWins.get_width() / 2, screen.get_height() / 2 - blueWins.get_height() / 2])
                pygame.display.update()
                winScreen = True
            while winScreen:
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_RETURN:
                        winScreen = False
    paused = True
    screen.fill([0, 0, 0])
    if first:  # On first run
        screen.blit(title, [screen.get_width() / 2 - title.get_width() / 2, screen.get_height() / 3])
        screen.blit(quitButton, [screen.get_width() / 2 - quitButton.get_width() / 2, screen.get_height() * 9 / 10 - quitButton.get_height()])
        screen.blit(playButton, [screen.get_width() / 2 - playButton.get_width() / 2, screen.get_height() * 9 / 10 - quitButton.get_height() - playButton.get_height()])
    else:
        screen.blit(pausedText, [screen.get_width() / 2 - pausedText.get_width() / 2, screen.get_height() / 3])
        screen.blit(quitButton, [screen.get_width() / 2 - quitButton.get_width() / 2, screen.get_height() * 9 / 10 - quitButton.get_height()])
        screen.blit(resetButton, [screen.get_width() / 2 - resetButton.get_width() / 2, screen.get_height() * 9 / 10 - quitButton.get_height() - resetButton.get_height()])
        screen.blit(resumeButton, [screen.get_width() / 2 - resumeButton.get_width() / 2, screen.get_height() * 9 / 10 - quitButton.get_height() - resetButton.get_height() - resumeButton.get_height()])
    pygame.display.update()
