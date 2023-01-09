import time
import pygame.time
from pygame.locals import *
from pygame import mixer
import sqlite3

# This is for storage of high scores.
conn = sqlite3.connect('GravioScores_database')
cursor = conn.cursor() # Create cursor to get values from a database.


pygame.init()
# Screen Variables
introduction = True

FrameHeight = 800  # Screen height
FrameWidth = 1300  # Screen width
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
geoUserBig = pygame.image.load("yifanChar.jpg")  # Change here
geoUser = pygame.transform.rotozoom(geoUserBig, 0, 0.525)
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
# cursor.execute('''INSERT INTO highScores (score) VALUES (?)''', (50,))
# conn.commit()


def runGame():
    userGravity = 3
    downUp = 1  # Frames increase going down, so a positive downUp means going down.
    running = True
    scroll = 0
    userScore = 0  # Default score - duh

    pressLock = False # lock the space key
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
            pressLock = False
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
                if event.key == pygame.K_SPACE and not pressLock:
                    downUp *= -1  # Flip gravity
                    pressLock = True # you can't move it now
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
# userEndScore = 85
mixer.music.stop()  # Stop Music

scoreBoard = Rect(650, 400, 500, 300)  # Default rectangle
scoreBoard.center = (650, 400)
pygame.draw.rect(screen, color_Dict["backGround"], scoreBoard)


endscore = scorefont.render('Your Score: ' + str(userEndScore), True, color_Dict["white"])

cursor.execute('''SELECT * FROM highScores ORDER BY score LIMIT 1''')
scores = cursor.fetchall()

if userEndScore > scores[0][0]: # If it beat the high score
    print("HIGH SCORE!")
    cursor.execute("""UPDATE highScores SET score = (?) WHERE score = (?)""", (userEndScore, scores[0][0]))  # Push rank down one (ex: change to rank 4 where rank = 3).
    conn.commit()
    # Now get the new score
    cursor.execute('''SELECT * FROM highScores ORDER BY score LIMIT 1''')
    scores = cursor.fetchall()
    congrats = scorefont.render("NEW HIGH SCORE!", True, color_Dict["white"])
    screen.blit(congrats, (scoreBoard.centerx - (congrats.get_width() // 2), scoreBoard.top + 30))
else:
    text = font.render('Nice Try!', True, color_Dict["white"])
    screen.blit(text, (scoreBoard.centerx - (text.get_width() // 2), scoreBoard.top + 30))

highScore = font.render('Top Score: ' + str(scores[0][0]), True, color_Dict["white"])

screen.blit(endscore, (scoreBoard.centerx - (endscore.get_width()//2), scoreBoard.top + 105))
screen.blit(highScore, (scoreBoard.centerx - (highScore.get_width()//2), scoreBoard.top + 155))

# Display the game over screen ... one last time.
pygame.display.update()
time.sleep(5.0)
pygame.quit()
