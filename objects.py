import pygame
import random

pygame.mixer.init()
wing_fx = pygame.mixer.Sound('Sounds/wing.wav')


class Grumpy:
	def __init__(self, win):
		self.win = win

		self.im_list = []
		bird_color = random.choice(['red', 'blue', 'yellow'])
		for i in range(1, 4):
			img = pygame.image.load(f'Assets/Grumpy/{bird_color}{i}.png')
			self.im_list.append(img)

		self.reset()

	def update(self):
		height = self.win.get_height()
		display_height = 0.80 * height

		# gravity
		self.vel += 0.3
		if self.vel >= 8:
			self.vel = 8
		if self.rect.bottom <= display_height:
			self.rect.y += int(self.vel)

		if self.alive:
			# jump
			keys = pygame.key.get_pressed()
			if keys[pygame.K_SPACE] and not self.jumped:
				wing_fx.play()
				self.jumped = True
				self.vel = -6
			if not keys[pygame.K_SPACE]:
				self.jumped = False

			self.flap_counter()
			self.image = pygame.transform.rotate(self.im_list[self.index], self.vel * -2)
		else:
			if self.rect.bottom <= display_height:
				self.theta -= 2
			self.image = pygame.transform.rotate(self.im_list[self.index], self.theta)

		self.win.blit(self.image, self.rect)

	def flap_counter(self):
		# animation
		self.counter += 1
		if self.counter > 5:
			self.counter = 0
			self.index += 1
		if self.index >= 3:
			self.index = 0

	def draw_flap(self):
		width = self.win.get_width()
		self.flap_counter()
		if self.flap_pos <= -10 or self.flap_pos > 10:
			self.flap_inc *= -1
		self.flap_pos += self.flap_inc
		self.rect.y += self.flap_inc
		self.rect.x = width // 2 - 20
		self.image = self.im_list[self.index]
		self.win.blit(self.image, self.rect)

	def reset(self):
		height = self.win.get_height()
		width = self.win.get_width()
		self.index = 0
		self.image = self.im_list[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = int(width * 0.2)
		self.rect.y = int(0.80 * height) // 2
		self.counter = 0
		self.vel = 0
		self.jumped = False
		self.alive = True
		self.theta = 0
		self.mid_pos = int(0.80 * height) // 2
		self.flap_pos = 0
		self.flap_inc = 1


class Base:
	def __init__(self, win):
		self.win = win
		width = self.win.get_width()
		height = self.win.get_height()
		display_height = int(0.80 * height)

		base_img = pygame.image.load('Assets/base.png')
		# Scale base to fit width and maintain aspect ratio
		base_height = base_img.get_height()
		scale_factor = width / base_img.get_width()
		new_height = int(base_height * scale_factor)
		self.image1 = pygame.transform.scale(base_img, (width, new_height))
		self.image2 = self.image1
		self.rect1 = self.image1.get_rect()
		self.rect1.x = 0
		self.rect1.y = display_height
		self.rect2 = self.image2.get_rect()
		self.rect2.x = width
		self.rect2.y = display_height

	def update(self, speed):
		width = self.win.get_width()
		self.rect1.x -= speed
		self.rect2.x -= speed

		if self.rect1.right <= 0:
			self.rect1.x = width - 5
		if self.rect2.right <= 0:
			self.rect2.x = width - 5

		self.win.blit(self.image1, self.rect1)
		self.win.blit(self.image2, self.rect2)


class Pipe(pygame.sprite.Sprite):
	def __init__(self, win, image, y, position):
		super(Pipe, self).__init__()

		width = win.get_width()
		self.win = win
		self.image = image
		self.rect = self.image.get_rect()
		pipe_gap = 100 // 2
		x = width

		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = (x, y - pipe_gap)
		elif position == -1:
			self.rect.topleft = (x, y + pipe_gap)
		self.position = position
		self.passed = False

	def update(self, speed):
		self.rect.x -= speed
		if self.rect.right < 0:
			self.kill()
		self.win.blit(self.image, self.rect)


class Score:
	def __init__(self, x, y, win):
		self.score_list = []
		for score in range(10):
			img = pygame.image.load(f'Assets/Score/{score}.png')
			self.score_list.append(img)
		self.x = x
		self.y = y

		self.win = win

	def update(self, score):
		score = str(score)
		for index, num in enumerate(score):
			self.image = self.score_list[int(num)]
			self.rect = self.image.get_rect()
			self.rect.topleft = (self.x - 15 * len(score) + 30 * index, self.y)
			self.win.blit(self.image, self.rect)
