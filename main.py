import time
import pygame.time
from pygame.locals import *
from pygame import mixer
import sqlite3

# This is for storage of high scores.
conn = sqlite3.connect('GravioScores_database')
cursor = conn.cursor()


pygame.init()
# Screen Variables
introduction = True

FrameHeight = 800
FrameWidth = 1300
screen = pygame.display.set_mode((FrameWidth, FrameHeight))
pygame.display.set_caption("Grav-io")  # The name of the game!
bg = pygame.image.load("customBackground.jpg")
bg = pygame.transform.scale(bg, (FrameWidth, FrameHeight))
clock = pygame.time.Clock()

# Length, Width of most of the screen


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
# userYSpeed = 0
# userScore = 0  # Default score - duh

# Text Stuff
pygame.font.init()  # initialize font
font = pygame.font.Font('freesansbold.ttf', 32)
scorefont = pygame.font.Font('freesansbold.ttf', 27)
# Gravity variables

mixer.music.play()
print("Jared says 'Hello world!'")  # My friend made me write this - also confirmation that this is working

def runGame():
    userGravity = 3
    downUp = 1  # Frames increase going down, so a positive downUp means going down.
    running = True
    scroll = 0
    userScore = 0  # Default score - duh

    # Block Variables
    rectShape = Rect(0, 375, 500, 50)  # This should be a rectangle of 500 X 50
    rectX = 0  # The x speed of the rectangle.
    rectSpeed = -10  # Rectangle speed as it goes to the left
    # Start the player
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
    return userScore


userEndScore = runGame()


mixer.music.stop()  # Stop Music

cursor.execute('''SELECT * FROM scores ORDER BY score LIMIT 5''')
scores = cursor.fetchall()


scoreBoard = Rect(650, 400, 500, 500)  # Default rectangle
scoreBoard.center = (650, 400)
pygame.draw.rect(screen, color_Dict["backGround"], scoreBoard)

text = font.render('Nice Try!', True, color_Dict["white"])
endscore = scorefont.render('Your Score: ' + str(userEndScore), True, color_Dict["white"])
highScore = font.render('Top Scores: ', True, color_Dict["white"])

# print(scores)
# print(scores[1])
# print(cursor.fetchall()[-1])
firstPlace = scorefont.render(('1. ' + scores[4][1] + ": " + str(scores[4][0])), True, color_Dict["white"])
secondPlace = scorefont.render(('2. ' + scores[3][1] + ": " + str(scores[3][0])), True, color_Dict["white"])
thirdPlace = scorefont.render(('3. ' + scores[2][1] + ": " + str(scores[2][0])), True, color_Dict["white"])
fourthPlace = scorefont.render(('4. ' + scores[1][1] + ": " + str(scores[1][0])), True, color_Dict["white"])
fifthPlace = scorefont.render(('5. ' + scores[0][1] + ": " + str(scores[0][0])), True, color_Dict["white"])

screen.blit(text, (scoreBoard.centerx - (text.get_width()//2), scoreBoard.top + 30))
screen.blit(endscore, (scoreBoard.centerx - (endscore.get_width()//2), scoreBoard.top + 80))
screen.blit(highScore, (scoreBoard.centerx - (highScore.get_width()//2), scoreBoard.top + 150))
screen.blit(firstPlace, (scoreBoard.centerx - (firstPlace.get_width()//2), scoreBoard.top + 190))
screen.blit(secondPlace, (scoreBoard.centerx - (secondPlace.get_width()//2), scoreBoard.top + 230))
screen.blit(thirdPlace, (scoreBoard.centerx - (thirdPlace.get_width()//2), scoreBoard.top + 270))
screen.blit(fourthPlace, (scoreBoard.centerx - (fourthPlace.get_width()//2), scoreBoard.top + 310))
screen.blit(fifthPlace, (scoreBoard.centerx - (fifthPlace.get_width()//2), scoreBoard.top + 350))

# Display the game over screen ... one last time.
pygame.display.update()
time.sleep(5.0)
pygame.quit()
