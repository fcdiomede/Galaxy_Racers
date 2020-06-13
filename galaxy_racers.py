import pygame
import time


bg = pygame.image.load('bg.jpg')
spaceship_img = [pygame.image.load('spacecraft_left.png'),pygame.image.load('spacecraft_right.png'),pygame.image.load('spacecraft_up.png'),pygame.image.load('spacecraft_down.png')]
cloud_img = pygame.image.load('cloud.png')

class spaceship(object):
	def __init__(self, x,y, dirx, diry,imgindex):
		self.x = x
		self.y = y
		self.dirx = diry
		self.diry = dirx
		self.vel = 5
		self.dir_index = imgindex
		self.smoke_trail = []
		self.smoke_count = 0
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)

	def draw(self,win):
		#draws the the smoke clouds
		for rectangle in self.smoke_trail:
			win.blit(cloud_img, (rectangle[0],rectangle[1]))

		#draw the spaceship
		win.blit(spaceship_img[self.dir_index], (self.x, self.y))


		#pygame.draw.rect(win, (255,0,0), self.hitbox,2)
		#commented out code that makes hitbox visible
	

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
			self.hitbox = (self.x + 6, self.y + 23 , 37, 60)
		

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
	if len(ship.smoke_trail) > 3:
		wall = ship.smoke_trail[:len(ship.smoke_trail)-3]
		enemy_wall = enemy.smoke_trail
		spaceship_rect = pygame.Rect(shiphitbox)
		if spaceship_rect.collidelist(wall) > -1 or spaceship_rect.collidelist(enemy_wall) > -1:
			return True

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

def showGameStartScreen(win, width, height):
	clock = pygame.time.Clock()
	win.blit(bg, (0,0))
	draw_text(win, "Galaxy Racers", 64, width / 2, height / 4)
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
	#change the class values for dirx, diry, and index

	next_posx = ship.x + ship.vel * ship.dirx
	next_posy = ship.y + ship.vel * ship.diry
	next_hitbox_location = (next_posx + 17, next_posy + 2, 31, 57)

	if ship.dirx == 0:
		combinations = [[-1,0,0], [1,0,1]]
	else:
		combinations = [[0,-1,2], [0,1,3]]

	if collision(ship, enemy_ship,ship.dirx, ship.diry, next_hitbox_location):
		for combo in combinations:
			if not collision(ship, enemy_ship, combo[0], combo[1], next_hitbox_location):
				ship.dirx = combo[0]
				ship.diry = combo[1]
				ship.dir_index = combo[2]
				break
			else:
				pass
		

	ship.x += ship.vel * ship.dirx
	ship.y += ship.vel * ship.diry
	ship.hitbox_pos()

def main():
	pygame.init()
	screen_width = 1000
	screen_height = 800
	win = pygame.display.set_mode((screen_width,screen_height))

	showGameStartScreen(win, screen_width, screen_height)

	player = spaceship(screen_width / 2, screen_height / 2 - 25,0, -1, 0)

	enemy = spaceship(screen_width / 2 , screen_height / 2 + 25 ,0, 1, 1)

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

		if collision(player, enemy, player.dirx, player.diry, player.hitbox):
			#if there is a collision, game must be over, go back to start screen
			if showGameStartScreen(win,screen_width,screen_height):
				#if player wants to play again, reset positions
				player = spaceship(screen_width / 2, screen_height / 2 - 25,0, -1, 0)
				enemy = spaceship(screen_width / 2 , screen_height / 2 + 25,0, 1, 1)

			else:
				pygame.quit()


			

main()