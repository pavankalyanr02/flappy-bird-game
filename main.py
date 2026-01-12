import pygame
import random

from objects import Grumpy, Pipe, Base, Score


pygame.init()
# Portrait logical resolution; SCALED+FULLSCREEN will fit to screen.
WIDTH, HEIGHT = 288, 512
SCREEN = (WIDTH, HEIGHT)
display_height = 0.80 * HEIGHT

# Open as a standard window (not fullscreen/scaled)
win = pygame.display.set_mode(SCREEN)


clock = pygame.time.Clock()
FPS = 60

# Title font for start screen
font_title = pygame.font.SysFont(None, 48, bold=True)

def draw_title(surface, text, x, y):
	# draw shadow layers for contrast
	shadow_color = (0, 0, 0)
	for dx, dy in ((2, 2), (1, 1), (3, 3)):
		img = font_title.render(text, True, shadow_color)
		rect = img.get_rect(center=(x + dx, y + dy))
		surface.blit(img, rect)
	# main bright text
	img = font_title.render(text, True, (255, 220, 0))
	rect = img.get_rect(center=(x, y))
	surface.blit(img, rect)



RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)



# Load backgrounds and scale to portrait resolution
bg1 = pygame.image.load('Assets/background-day.png')
bg2 = pygame.image.load('Assets/background-night.png')
bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))
bg2 = pygame.transform.scale(bg2, (WIDTH, HEIGHT))

bg = random.choice([bg1, bg2])

im_list = [pygame.image.load('Assets/pipe-green.png'), pygame.image.load('Assets/pipe-red.png')]
pipe_img = random.choice(im_list)

gameover_img = pygame.image.load('Assets/gameover.png')
gameover_img = pygame.transform.scale(gameover_img, (160, 80))
flappybird_img = pygame.image.load('Assets/flappybird.png')
flappybird_img = pygame.transform.scale(flappybird_img, (80, 80))



die_fx = pygame.mixer.Sound('Sounds/die.wav')
hit_fx = pygame.mixer.Sound('Sounds/hit.wav')
point_fx = pygame.mixer.Sound('Sounds/point.wav')
swoosh_fx = pygame.mixer.Sound('Sounds/swoosh.wav')
wing_fx = pygame.mixer.Sound('Sounds/wing.wav')



pipe_group = pygame.sprite.Group()
base = Base(win)
score_img = Score(WIDTH // 2, 50, win)
grumpy = Grumpy(win)



base_height = 0.80 * HEIGHT
speed = 0
game_started = False
game_over = False
restart = False
score = 0
start_screen = True
pipe_frequency = 1600
space_pressed = False

running = True
while running:
	win.blit(bg, (0, 0))

	if start_screen:
		speed = 0
		grumpy.draw_flap()
		base.update(speed)

		flappybird_rect = flappybird_img.get_rect(center=(WIDTH // 2, 80))
		win.blit(flappybird_img, flappybird_rect)
        # Only the image-based FLAPPY BIRD remains; removed duplicate text
	else:

		if game_started and not game_over:

			next_pipe = pygame.time.get_ticks()
			if next_pipe - last_pipe >= pipe_frequency:
				y = display_height // 2
				pipe_pos = random.choice(range(-100, 100, 4))
				height = y + pipe_pos

				top = Pipe(win, pipe_img, height, 1)
				bottom = Pipe(win, pipe_img, height, -1)
				pipe_group.add(top)
				pipe_group.add(bottom)
				last_pipe = next_pipe

		pipe_group.update(speed)
		base.update(speed)
		grumpy.update()
		score_img.update(score)

		if pygame.sprite.spritecollide(grumpy, pipe_group, False) or grumpy.rect.top <= 0:
			game_started = False
			if grumpy.alive:
				hit_fx.play()
				die_fx.play()
			grumpy.alive = False
			grumpy.theta = grumpy.vel * -2

		if grumpy.rect.bottom >= display_height:
			speed = 0
			game_over = True

		for pipe in pipe_group:
			if pipe.position == -1 and not pipe.passed and grumpy.rect.left > pipe.rect.right and grumpy.alive:
				pipe.passed = True
				score += 1
				point_fx.play()

	if not grumpy.alive:
		gameover_rect = gameover_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
		win.blit(gameover_img, gameover_rect)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
					event.key == pygame.K_q:
				running = False
			if event.key == pygame.K_SPACE:
				if start_screen:
					game_started = True
					speed = 2
					start_screen = False

					game_over = False

					last_pipe = pygame.time.get_ticks() - pipe_frequency
					next_pipe = 0
					pipe_group.empty()

					speed = 2
					score = 0

				if game_over:
					start_screen = True
					grumpy = Grumpy(win)
					pipe_img = random.choice(im_list)
					bg = random.choice([bg1, bg2])


	clock.tick(FPS)
	pygame.display.update()
pygame.quit()
