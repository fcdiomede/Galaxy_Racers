import pygame
import time
import random

bg = pygame.image.load('bg.jpg')
spaceship_img = [pygame.image.load('spacecraft_left.png'),pygame.image.load('spacecraft_right.png'),pygame.image.load('spacecraft_up.png'),pygame.image.load('spacecraft_down.png')]
cloud_img = pygame.image.load('cloud.png')
evil_spaceship_img = [pygame.image.load('evil_spacecraft_left.png'),pygame.image.load('evil_spacecraft_right.png'),pygame.image.load('evil_spacecraft_up.png'),pygame.image.load('evil_spacecraft_down.png')]
evil_cloud_img = pygame.image.load('evil_cloud.png')

class spaceship(object):
	def __init__(self, x,y, dirx, diry,imgindex,shipimg,cloudimg):
		self.x = x
		self.y = y
		self.dirx = diry
		self.diry = dirx
		self.vel = 5
		self.dir_index = imgindex
		self.smoke_trail = []
		self.smoke_count = 0
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)
		self.shipimg = shipimg
		self.cloudimg = cloudimg

	def draw(self,win):
		#draws the the smoke clouds
		for rectangle in self.smoke_trail:
			win.blit(self.cloudimg, (rectangle[0],rectangle[1]))
			#makes hitbox visible
			#pygame.draw.rect(win, (255,0,0), rectangle,2)

		#draw the spaceship
		win.blit(self.shipimg[self.dir_index], (self.x, self.y))

		#makes hitbox visible
		#pygame.draw.rect(win, (255,0,0), self.hitbox,2)

	def hitbox_pos(self):
		#adjusts hitbox positioning depending on the spaceship direction
		#if moving left
		if self.dirx == -1:
			self.hitbox = (self.x + 13, self.y + 6, 60, 37)
		#if moving right
		elif self.dirx == 1:
			self.hitbox = (self.x + 23, self.y + 6 ,60, 37)
		#if moving up
		elif self.diry == -1:
			self.hitbox = (self.x + 6, self.y + 13,37, 60)
		#else, I must be moving down
		else:
			self.hitbox = (self.x + 6, self.y + 23, 37, 60)
		
	def move(self):
		keys = pygame.key.get_pressed()

		for key in keys:
			if keys[pygame.K_LEFT] and self.dirx != 1:
				self.dirx = -1
				self.diry = 0
				self.dir_index = 0
			elif keys[pygame.K_RIGHT] and self.dirx != -1:
				self.dirx = 1
				self.diry = 0
				self.dir_index = 1
			elif keys[pygame.K_UP] and self.diry != 1:
				self.dirx = 0
				self.diry = -1
				self.dir_index = 2
			elif keys[pygame.K_DOWN] and self.diry != -1:
				self.dirx = 0
				self.diry = 1
				self.dir_index = 3

		#modify where I am based on direction I am moving and velocity
		self.x += self.vel * self.dirx
		self.y += self.vel * self.diry

		#modify where the hitbox is located
		self.hitbox_pos()

	def smoke(self):
		#adds in smoke cloud positions to a list
		self.smoke_count += 1
		if self.smoke_count % 7 == 0:
			self.smoke_trail.append(pygame.Rect(self.x, self.y,30,30))

def collision(ship, enemy, xdirection, ydirection, shiphitbox):
	#if moving left, check if I've hit the leftmost wall
	if xdirection == -1 and shiphitbox[0] <= 0:
		return True
	#if moving right, check if I've hit the rightmost wall
	elif xdirection == 1 and shiphitbox[0] >= 980:
		return True
	#if moving up, check if I've hit the upper wall
	elif ydirection == -1 and shiphitbox[1] <= 0:
		return True
	#else, I must be moving down, check if I've hit the lower wall
	elif ydirection == 1 and shiphitbox[1] >= 780:
		return True
	
	#check if I've hit any of the smoke clouds either I've or the enemy ship has left
	if len(ship.smoke_trail) > 5:
		wall = ship.smoke_trail[:len(ship.smoke_trail)-5]
		enemy_wall = enemy.smoke_trail
		spaceship_rect = pygame.Rect(shiphitbox)
		if spaceship_rect.collidelist(wall) > -1 or spaceship_rect.collidelist(enemy_wall) > -1:
			return True

	return False

def redrawGameWindow(win, player, enemy):
	win.blit(bg, (0,0))
	player.draw(win)
	enemy.draw(win)
	pygame.display.update()

def draw_text(surf, text, size, x, y):
    font = pygame.font.SysFont('arial', 50, True)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def showGameStartScreen(win, width, height, text):
	clock = pygame.time.Clock()
	win.blit(bg, (0,0))
	draw_text(win, text, 64, width / 2, height / 4)
	draw_text(win, "Use arrow keys to move", 22, width/ 2, height / 2)
	draw_text(win, "Press a key to begin", 18, width / 2, height * 3 / 4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return False
			if event.type == pygame.KEYUP:
				waiting = False
				return True

def computerMovement(ship, enemy_ship):

	current_direction = [ship.dirx,ship.diry,ship.dir_index]
	if ship.dirx == 0:
		possible_directions = [current_direction,[-1,0,0], [1,0,1]]
	else:
		possible_directions = [current_direction,[0,-1,2], [0,1,3]]

	valid_directions = []

	for direction in possible_directions:
		#mulitply the velocity so that I look a bit ahead and give the ship time to turn
		next_posx = (ship.x + (ship.vel * 1.7) * direction[0]) 
		next_posy = (ship.y + (ship.vel * 1.7) * direction[1]) 

		if direction[0] == -1:
			direction_hitbox = (next_posx + 13, next_posy + 6, 60, 37)
		#if moving right
		elif direction[0] == 1:
			direction_hitbox = (next_posx + 23, next_posy + 6, 60, 37)
		#if moving up
		elif direction[1] == -1:
			direction_hitbox = (next_posx + 6, next_posy + 13, 37, 60)
		#else, I must be moving down
		else:
			direction_hitbox = (next_posx + 6, next_posy + 23, 37, 60)

		if not collision(ship, enemy_ship,direction[0], direction[1], direction_hitbox):
			valid_directions.append(direction)
	
	#favor current direction, with possibility of going in a random direction
	if current_direction in valid_directions:
		random_num = random.randint(0,300)
		if random_num < 1:
			direction = random.choice(valid_directions)
			ship.dirx = direction[0]
			ship.diry = direction[1]
			ship.dir_index = direction[2]
	elif valid_directions == []:
		pass
	else:
		#if the current direction is not in the list, it would cause a collision
		#so pick a random direction of the possible direction
		direction = random.choice(valid_directions)
		ship.dirx = direction[0]
		ship.diry = direction[1]
		ship.dir_index = direction[2]

	ship.x += ship.vel * ship.dirx
	ship.y += ship.vel * ship.diry
	ship.hitbox_pos()

def main():
	pygame.init()
	screen_width = 1000
	screen_height = 800
	win = pygame.display.set_mode((screen_width,screen_height))

	showGameStartScreen(win, screen_width, screen_height, "Galaxy Racers")

	player = spaceship(screen_width / 2, screen_height / 2 - 25,0, -1, 0, spaceship_img, cloud_img)

	enemy = spaceship(screen_width / 2 , screen_height / 2 + 25 ,0, 1, 1, evil_spaceship_img, evil_cloud_img)

	# Variable to keep the main loop running
	running = True

	# Main loop
	while running:
		# Did the user click the window close button? If so, stop the loop.
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		player.move()
		player.smoke()
		computerMovement(enemy, player)
		enemy.smoke()
		redrawGameWindow(win,player,enemy)


		if collision(player, enemy, player.dirx, player.diry, player.hitbox) or collision(enemy, player, enemy.dirx, enemy.diry, enemy.hitbox):
			if collision(player, enemy, player.dirx, player.diry, player.hitbox):
				display = "You ran out of sky! Better luck next time?"
			else:
				display = "Sweet flying! You win! Play again?"

			if showGameStartScreen(win,screen_width,screen_height, display):
			 	#if player wants to play again, reset positions
				player = spaceship(screen_width / 2 - 30, screen_height / 2, 0, -1, 0,spaceship_img, cloud_img)
				enemy = spaceship(screen_width / 2 + 30, screen_height / 2, 0, 1, 1, evil_spaceship_img, evil_cloud_img)

			else:
			 	pygame.quit()


main()