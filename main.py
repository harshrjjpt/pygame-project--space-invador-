import pygame
import random
import math
from pygame import mixer



pygame.init()

#SCREEN
screen = pygame.display.set_mode((800,600))

#TITLE
pygame.display.set_caption("NEMO INVADORS")

#BACKGROUND
background = pygame.image.load("background.jpg")
mixer.music.load("background.wav")
mixer.music.play(-1)
#LOGO
logo = pygame.image.load("block.jpg")
pygame.display.set_icon(logo)

#BONE
#when bone_state = ready: bone n0t displaying
				 #if = launch : bone is moving 
bone_image = pygame.image.load("bone.png")
boneX = 0
boneY = 490

boneX_change = 0
boneY_change = 1.2
bone_state = "ready"

#score
score_num = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

def show_score(x,y):
	score = font.render("score :" + str(score_num),True, (255, 255, 255))
	screen.blit(score, (x, y))

#PLAYER
nemo = pygame.image.load("player.png")
playerX = 360
playerY = 490

playerX_change = 0
playerY_change = 0

#ENEMY
cat = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies_num = 8

for i in range(enemies_num):
	cat.append(pygame.image.load("enemy.png"))	
	enemyX.append(random.randint(0,760))
	enemyY.append(random.randint(20,250))
	enemyX_change.append(0.2)
	enemyY_change.append(40)

#player movement func
def player(x,y):
	screen.blit(nemo, (x,y))
#enemy movement func
def enemy(x, y, i):
	screen.blit(cat[i], (x,y))
#bone func
def launch_bone(x,y):
	global bone_state
	bone_state = "launch"
	screen.blit(bone_image, (x+13, y))

#COLLISION
def is_collision(enemyX, enemyY, boneX, boneY):
	distance = math.sqrt((math.pow(enemyX-boneX, 2)) + (math.pow(enemyY-boneY, 2)))
	if distance < 30:
		return True
	else:
		return False  	


running = True
while running:
	screen.fill((255, 153, 252))
	screen.blit(background, (0,0))
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False


		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				playerX_change = 0.3
			elif event.key == pygame.K_LEFT:
				playerX_change = -0.3
			elif event.key == pygame.K_UP:
				playerY_change = -0.3
			elif event.key == pygame.K_DOWN:
				playerY_change = 0.3
			elif event.key == pygame.K_SPACE:
				bone_sound = mixer.Sound("throw_sound.wav")
				bone_sound.play()
				if bone_state is "ready":
					#matching x coordinate with player
					boneX = playerX
					launch_bone(boneX, boneY)	

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				playerX_change = 0
			elif event.key == pygame.K_LEFT:
				playerX_change = 0
			elif event.key == pygame.K_UP:
				playerY_change = 0
			elif event.key == pygame.K_DOWN:
				playerY_change = 0

	playerX += playerX_change
	playerY += playerY_change
#player boundary restriction
	if playerX <= 0:
		playerX = 0
	elif playerX >= 760:
		playerX = 760
	elif playerY >= 560:
		playerY = 560
	elif playerY <= 400:
		playerY = 400        	

#enemy movement
	for i in range(enemies_num):
		enemyX[i] += enemyX_change[i]

		if enemyX[i] <= 0:
			enemyX_change[i] = 0.3
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 760:
			enemyX_change[i] = -0.3
			enemyY[i] += enemyY_change[i]
	  
		#collision
		collision = is_collision(enemyX[i], enemyY[i], boneX, boneY)
		if collision:
			collision_sound = mixer.Sound("collisionn.wav")
			collision_sound.play()
			boneY = 490
			bone_state = "ready"
			score_num += 10
			enemyX[i] = random.randint(0, 760)
			enemyY[i] = random.randint(20,250)

		enemy(enemyX[i], enemyY[i], i)	

#bullet movement
	if boneY <= 0:
		boneY = 490
		bone_state = "ready"


	if bone_state is "launch":
		launch_bone(boneX, boneY)
		boneY -= boneY_change



		


	
	

	player(playerX, playerY)    
	show_score(textX, textY)	   
	pygame.display.update()