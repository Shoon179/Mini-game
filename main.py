import pygame
from sys import exit
from random import randint, choice

class Wanderer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        wanderer_run1 = pygame.image.load('assets/character/idle.png').convert_alpha()
        wanderer_run2 = pygame.image.load('assets/character/run1.png').convert_alpha()
        wanderer_run3 = pygame.image.load('assets/character/run2.png').convert_alpha()
        self.wanderer_run = [wanderer_run1,wanderer_run2,wanderer_run3]
        #jumping wanderer
        wanderer_jump1 = pygame.image.load('assets/character/jump1.png').convert_alpha()
        wanderer_jump2 = pygame.image.load('assets/character/jump2.png').convert_alpha()
        self.wanderer_jump = [wanderer_jump1,wanderer_jump2]

        self.wanderer_index = 0
        self.gravity = 0
        self.image = pygame.transform.scale(self.wanderer_run[self.wanderer_index], (80,90))
        self.rect = self.image.get_rect(midbottom = (70,350))
        self.jump_sound = pygame.mixer.Sound('assets/sound/jump.wav')
        self.jump_sound.set_volume(0.4)

    def animation(self):
        if self.rect.bottom < 350:
            self.wanderer_index += 0.1
            if self.wanderer_index > len(self.wanderer_jump):
                self.wanderer_index = 0
            self.image = pygame.transform.scale(self.wanderer_jump[int(self.wanderer_index)], (80,90))
        else:
            self.wanderer_index += 0.1
            if self.wanderer_index > len(self.wanderer_run):
                self.wanderer_index = 0
            self.image = pygame.transform.scale(self.wanderer_run[int(self.wanderer_index)], (80,90))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 350:
            self.gravity = -21
            self.jump_sound.play()
            
    def add_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 350:
            self.rect.bottom = 350
    
    def update(self):
        self.animation()
        self.input()
        self.add_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'cactus':
            cactus = pygame.transform.scale(pygame.image.load('assets/obstacles/cactus.png').convert_alpha(), (40,45))
            self.image = cactus
        elif type == 'crate':
            crate = pygame.transform.scale(pygame.image.load('assets/obstacles/crate.png').convert_alpha(), (40,45))
            self.image = crate
        elif type == 'spike':
            spike = pygame.transform.scale(pygame.image.load('assets/obstacles/Spike.png').convert_alpha(), (50,60))
            self.image = spike
        else:
            stone = pygame.transform.scale(pygame.image.load('assets/obstacles/stone.png').convert_alpha(), (30,15))
            self.image = stone
        self.rect = self.image.get_rect(bottomright = (randint(850, 1200),350))

    def remove_obstacle(self):
        if self.rect.x <= -50:
            self.kill()

    def update(self):
        self.rect.x -= 4
        self.remove_obstacle()

class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        star= pygame.transform.scale(pygame.image.load('assets/rewards/star.png').convert_alpha(), (35,35))
        self.image = star
        self.rect = self.image.get_rect(midright = (randint(850,1200), 190))

    def remove_star(self):
        if self.rect.x <= -50:
            self.kill()

    def update(self):
        self.rect.x -= 3.5
        self.remove_star()

class Dia(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        dia = pygame.transform.scale(pygame.image.load('assets/rewards/dia.png').convert_alpha(), (35,35))
        self.image = dia
        self.rect = self.image.get_rect(midright = (randint(850,1200), 150))

    def remove_star(self):
        if self.rect.x <= -50:
            self.kill()

    def update(self):
        self.rect.x -= 3.5
        self.remove_star()

def collision():
    if pygame.sprite.spritecollide(runner.sprite, obstacle_gp,False):
        gameover_sound.play()
        obstacle_gp.empty()
        star_reward.empty()
        dia_reward.empty()
        return False
    else: 
        return True

def display_score():
    survival_time = int(pygame.time.get_ticks() / 1000) - start_time 
    score_surf = font1.render(f'Survival Time: {survival_time}s', False, (250, 15, 15))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf,score_rect)
    return survival_time

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Wanderer')
clock = pygame.time.Clock()
font1 = pygame.font.Font('assets/font/PressStart2P-Regular.ttf', 20)
font2 = pygame.font.Font('assets/font/Pixeltype.ttf', 30)
game_active = False
start_time = 0
score = 0
dia_num = 0
star_num = 0

runner = pygame.sprite.GroupSingle()
runner.add(Wanderer())
obstacle_gp = pygame.sprite.Group()
dia_reward = pygame.sprite.Group()
star_reward = pygame.sprite.Group()
#idle wanderer
wanderer_idle = pygame.transform.scale(pygame.image.load('assets/character/idle.png').convert_alpha(), (120,130))
wanderer_idle_rect = wanderer_idle.get_rect(center = (400, 200))

#dead wanderer
wanderer_dead = pygame.transform.scale(pygame.image.load('assets/character/dead.png').convert_alpha(), (120,130))
wanderer_dead_rect = wanderer_dead.get_rect(center = (400,150))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,2500)

dia_timer = pygame.USEREVENT + 2
pygame.time.set_timer(dia_timer, 8000)

star_timer = pygame.USEREVENT + 3
pygame.time.set_timer(star_timer, 5000)

#background
sky_surface = pygame.transform.scale(pygame.image.load('assets/bg/runtime_bg.png').convert(), (800,400))
ground_surface = pygame.image.load('assets/bg/ground.png').convert()
end_screen = pygame.transform.scale(pygame.image.load('assets/bg/sky.png').convert(), (800,400))

#sound
reward_sound = pygame.mixer.Sound('assets/sound/reward_pickup.wav')
reward_sound.set_volume(0.6)
gameover_sound = pygame.mixer.Sound('assets/sound/gameover.wav')

#game_message
game_name = font1.render('WANDERER', False, (250, 15, 15))
game_name_rect = game_name.get_rect(center = (400, 100))

gameover_text = font1.render('GAME OVER', False,(250, 15, 15))
gameover_text_rect = gameover_text.get_rect(center = (400,50))

start_text = font1.render('To Start: Press "Space"', False, (250, 15, 15))
start_text_rect = start_text.get_rect(center = (400,300))

restart_text = font2.render('To Restart: Press "Space"', False, (103, 2, 235))
restart_text_rect = restart_text.get_rect(center = (400, 350))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_gp.add(Obstacle(choice(['cactus', 'crate', 'spike', 'stone'])))
            if event.type == dia_timer:
                dia_reward.add(Dia())
            if event.type == star_timer:
                star_reward.add(Star())
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                star_num = 0
                dia_num = 0
                start_time = int(pygame.time.get_ticks()/1000)
                runner.sprite.rect.bottom = 350

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,350))
        score = display_score()

        runner.draw(screen)
        runner.update()

        obstacle_gp.draw(screen)
        obstacle_gp.update()
        
        dia_reward.draw(screen)
        dia_reward.update()
        if pygame.sprite.spritecollide(runner.sprite, dia_reward, True):
            dia_num += 1
            reward_sound.play()

        star_reward.draw(screen)
        star_reward.update()
        if pygame.sprite.spritecollide(runner.sprite, star_reward, True):
            star_num += 1
            reward_sound.play()

        game_active = collision()
    else:
        screen.blit(end_screen, (0,0))
        if score == 0:
            screen.blit(game_name,game_name_rect)
            screen.blit(wanderer_idle,wanderer_idle_rect)
            screen.blit(start_text,start_text_rect)

        else:
            screen.blit(end_screen, (0,0))
            screen.blit(wanderer_dead,wanderer_dead_rect)
            screen.blit(gameover_text,gameover_text_rect)
            survival_msg = font1.render(f'Survival Time: {score} s', False, (250, 15, 15))
            survial_msg_rect = survival_msg.get_rect(center = (400,250))
            screen.blit(survival_msg, survial_msg_rect)
        
            dia_text = font1.render(f'Diamond: {dia_num}', False, (252, 98, 3))
            dia_text_rect = dia_text.get_rect(center = (250, 300))
            screen.blit(dia_text,dia_text_rect)
            star_text = font1.render(f'Star: {star_num}', False, (252, 98, 3))
            star_text_rect = star_text.get_rect(bottomright = (650, 308))
            screen.blit(star_text,star_text_rect)
            
            screen.blit(restart_text, restart_text_rect)

    pygame.display.update()
    clock.tick(60)
