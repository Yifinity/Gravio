import time
import pygame.time
from pygame.locals import *
from pygame import mixer
import sqlite3

# This is for storage of high scores.


pygame.init()

# Screen Variables
introduction = True
running = True
FrameHeight = 800
FrameWidth = 1300
screen = pygame.display.set_mode((FrameWidth, FrameHeight))
pygame.display.set_caption("Grav-io")  # The name of the game!
bg = pygame.image.load("customBackground.jpg")
bg = pygame.transform.scale(bg, (FrameWidth, FrameHeight))
clock = pygame.time.Clock()

# Length, Width of most of the screen
scroll = 0

color_Dict = {
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
    "backGround": (55, 45, 125)
}

# Start mixer - Music!
mixer.init()
mixer.music.load("twentyfive.mp3")
mixer.music.set_volume(0.4)

# User Definitions
geoUserBig = pygame.image.load("customUser.png")  # Change here
geoUser = pygame.transform.rotozoom(geoUserBig, 0, 0.75)
user = geoUser.get_rect()  # Creates a rectangular region - haha get rect
user.center = 84, 350  # 116 - 136 on actual coordinates
userXSpeed = 0  # Default Speeds are zero
userYSpeed = 0
userScore = 0  # Default score - duh

# Text Stuff
pygame.font.init()  # initialize font
font = pygame.font.Font('freesansbold.ttf', 32)

# Gravity variables
gravity = 0  # Should start at zero.
userGravity = 3
downUp = 1  # Frames increase going down, so a positive downUp means going down.

# Block Variables
rectShape = Rect(0, 375, 500, 50)  # This should be a rectangle of 500 X 50
rectX = 0  # The x speed of the rectangle.
rectSpeed = -10  # Rectangle speed as it goes to the left
# Start the player

mixer.music.play()
print("Jared says 'Hello world!'")  # My friend made me write this - also confirmation that this is working

while running:
    screen.blit(bg, (scroll, 0))
    screen.blit(bg, (FrameWidth + scroll, 0))
    scroll -= 4  # Shift to the left
    if scroll == -FrameWidth:
        screen.blit(bg, (FrameWidth + scroll, 0))
        scroll = 0
    # screen.(color_Dict["backGround"])  # Requires A tuple
    pygame.draw.rect(screen, color_Dict["yellow"], rectShape)  # Draws the rectangle
    screen.blit(geoUser, user)  # merge the image and the rect together

    score = font.render("Score: " + str(userScore), True, color_Dict["white"], None)
    scoreRect = score.get_rect()
    screen.blit(score, scoreRect)  # Merge text and rect

    # Rectangle Function
    if rectShape.right < 0:  # When rectangle hits the end - the end of a level.
        rectShape = Rect(1250, 375, 1200, 40)
        userScore = userScore + 1  # Increase the score.
    else:
        rectX = rectSpeed

    if (user.right <= rectShape.right and user.left >= rectShape.left) and (user.bottom == rectShape.top or user.top == rectShape.bottom):
        gravity = 0
    else:
        gravity = userGravity * downUp  # Gravity concept

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                downUp *= -1  # Flip gravity
                # downUpHolder *= -1
    if user.bottom > FrameHeight or user.top < 0:
        running = not running

    userYSpeed = gravity
    rectShape.move_ip(rectX, 0)
    user.move_ip(userXSpeed, userYSpeed)  # Move
    pygame.display.update()
    clock.tick(200)

mixer.music.stop()  # Stop Music

# End stuff Create text
# text = font.render('You lost; you\'re a loser! Score: ' + str(userScore), True, color_Dict["white"], color_Dict["backGround"])
# Jacob wrote that ^

scoreBoard = Rect(650, 400, 500, 500)  # Default rectangle
scoreBoard.center = (650, 400)
pygame.draw.rect(screen, color_Dict["backGround"], scoreBoard)

text = font.render('Nice Try!', True, color_Dict["white"])
score = font.render('Your Score: ' + str(userScore), True, color_Dict["white"])
highScore = font.render('Top Scores: ' + str(userScore), True, color_Dict["white"])

textRect = text.get_rect()
scoreRect = score.get_rect()
highScoreRect = highScore.get_rect()

textRect.center = (scoreBoard.centerx, scoreBoard.top + 50)
scoreRect.center = (scoreBoard.centerx, textRect.top + 60)
highScoreRect.center = (scoreBoard.centerx, scoreRect.top + 100)

screen.blit(text, textRect)
screen.blit(score, scoreRect)
screen.blit(highScore, highScoreRect)


# Display the game over screen ... one last time.
pygame.display.update()
time.sleep(1.0)
pygame.quit()
