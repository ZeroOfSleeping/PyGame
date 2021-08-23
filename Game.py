import os
import pygame
import random
from pygame import draw

# 固定變數
HIGH = 400
WITH = 800
FPS = 60
offset = 80 

# 初始設定
pygame.init()
pygame.display.set_caption("奮Game")
screen = pygame.display.set_mode((WITH,HIGH))
clock = pygame.time.Clock()
font_name = os.path.join("kaiu.ttf")

# 載入圖片
BG_img = pygame.image.load(os.path.join("img", "BG.png")).convert() 
Player_img = []
for i in range(4):
    Player_img.append(pygame.image.load(os.path.join("img", f"Player{i}.png")).convert())
Fire_img = pygame.image.load(os.path.join("img", "Fire.png")).convert()
Rock_img = pygame.image.load(os.path.join("img", "Rock.png")).convert()
Hay_img = pygame.image.load(os.path.join("img", "Hay.png")).convert()
Gadgat_img = {}
Gadgat_img['HPO'] = pygame.image.load(os.path.join("img", "HP.png")).convert()
Gadgat_img['PWO'] = pygame.image.load(os.path.join("img", "PW.png")).convert()
Logo_img = pygame.image.load(os.path.join("img", "Logo.png")).convert()
pygame.display.set_icon(pygame.transform.scale(Logo_img,(10,10)))

# UI
def draw_init():
    screen.blit(pygame.transform.scale(BG_img,(800,400)), (0, 0))
    draw_Text(screen, '歡迎來到糞Game', 60, WITH/2, HIGH/4)
    draw_Text(screen, '↑ 跳躍 空白發射火球', 60, WITH/2, HIGH/2)
    draw_Text(screen, '任意鍵開始遊戲', 60, WITH/2, HIGH*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False     
def draw_GameOver():
    screen.blit(pygame.transform.scale(BG_img,(800,400)), (0, 0))
    draw_Text(screen, 'Game Over', 60, WITH/2, HIGH/4)
    draw_Text(screen, str(score), 60, WITH/2, HIGH/2)
    draw_Text(screen, '按任意鍵 重新開始遊戲', 60, WITH/2, HIGH*3/4)
    pygame.display.update()
    game_over = True
    while game_over:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                game_over = False     
                return False  
def draw_HP(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100 
    BAR_HEIGHT = 10
    fill = (hp/100)* BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (200,0,0), fill_rect)
def draw_Power(surf, power, x, y):
    if power < 0:
        power = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (power/100)* BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, (255,255,0), fill_rect)
def draw_Text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surf.blit(text_surface, text_rect)

# 物體
class Player(pygame.sprite.Sprite): 
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Player_img[0],(132,137))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (100,HIGH-offset)
        self.POWER = 100
        self.HP = 100
        self.form = 0
        self.last_time = pygame.time.get_ticks()
        self.delay_time = 100

    def update(self):
        now = pygame.time.get_ticks()
        if self.POWER > 0 and key_box[pygame.K_UP]:
            self.POWER -= 1
            self.rect.centery -= 50
            if now - self.last_time > self.delay_time:
                self.last_time = now
                self.image = pygame.transform.scale(Player_img[random.choice([2,3])],(132,137))
                self.image.set_colorkey((255,255,255))
            if self.rect.centery < HIGH/3:
                self.rect.centery = HIGH/3
            if self.POWER < 0:
                self.POWER = 0
        elif self.POWER <= 0 or self.rect.centery == HIGH-offset:
            self.rect.centery += 18
            if self.rect.centery > HIGH-offset:
                self.rect.centery = HIGH-offset
                if now - self.last_time > self.delay_time:
                    self.last_time = now
                    self.image = pygame.transform.scale(Player_img[random.choice([0,1])],(132,137))
                    self.image.set_colorkey((255,255,255))                
                    self.POWER += 5     
                    if self.POWER > 100:
                        self.POWER = 100
        else:
            self.rect.centery += 18              
            if self.rect.centery > HIGH-offset:
                self.rect.centery = HIGH-offset
                if now - self.last_time > self.delay_time:
                    self.last_time = now
                    self.image = pygame.transform.scale(Player_img[random.choice([0,1])],(132,137))
                    self.image.set_colorkey((255,255,255))  
                    self.POWER += 5
                    if self.POWER > 100:
                        self.POWER = 100            
    def shoot(self):
        fire = Fire(self.rect.right ,self.rect.top + 20)
        all_sprites.add(fire)
        fires.add(fire)
class Haystack(pygame.sprite.Sprite):
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image_oring = Hay_img
        self.image_oring.set_colorkey((255,255,255))
        self.image = self.image_oring.copy()
        self.rect = self.image.get_rect()
        self.rect.x = WITH + random.randrange(0, 100)
        self.rect.y = random.choice([250,60])
        self.degree = 0

    def rotate(self):
        self.degree += 3
        self.image = pygame.transform.rotate(self.image_oring,self.degree)

    def update(self):
        self.rotate()
        self.rect.x -= random.randrange(1, 15)
        if self.rect.right < 0:
            self.image_oring = Hay_img
            self.image_oring.set_colorkey((255,255,255))
            self.image = self.image_oring.copy()
            self.rect = self.image.get_rect()
            self.rect.x = WITH + random.randrange(0, 100)
            self.rect.y = random.choice([250,60])
            self.degree = 0 
class Rock(pygame.sprite.Sprite):
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Rock_img,(random.choice([(40,40),(80,80)])))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = WITH + random.randrange(-10, 300)
        self.rect.bottom = HIGH - 20

    def update(self):
        self.rect.x -= 5
        if self.rect.left < 0:
            self.image = pygame.transform.scale(Rock_img,(random.choice([(40,40),(80,80)])))
            self.image.set_colorkey((255,255,255))
            self.rect = self.image.get_rect()
            self.rect.x = WITH + random.randrange(-10, 300)
            self.rect.bottom = HIGH - 20
class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Fire_img,(60,60))
        self.image.set_colorkey((255,255,255)) 
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    
    def update(self):
        self.rect.x += 12
        if self.rect.left > WITH:
            self.kill()          
class Gadgat(pygame.sprite.Sprite):
    def __init__(self, center): 
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['HPO', 'PWO'])
        self.image = pygame.transform.scale(Gadgat_img[self.type],(40,40))
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        # if self.type == "PWO":
        #     self.rect.x -= 10 
        # else:
        self.rect.x -= 10
        self.rect.y += 10

        if self.rect.left < 0:
            self.kill()  
        if self.rect.bottom > HIGH - offset:
            self.rect.bottom = HIGH - offset

# 群組建立                
all_sprites = pygame.sprite.Group()
haystacks = pygame.sprite.Group()
rocks = pygame.sprite.Group()
fires = pygame.sprite.Group()
gadgats = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
score = 0
for i in range(random.randrange(2, 3)):
    haystack = Haystack()
    all_sprites.add(haystack)
    haystacks.add(haystack)
for i in range(random.randrange(2, 3)):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# 主程式     
game_over = False
show_init = True
running = True    
while running:
    if show_init:
        exit = draw_init()
        if exit:
            break
        show_init = False
    elif game_over:
        exit = draw_GameOver() 
        if exit:
            break
        game_over = False
        all_sprites = pygame.sprite.Group()
        haystacks = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        fires = pygame.sprite.Group()
        gadgats = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        score = 0
        for i in range(random.randrange(2, 3)):
            haystack = Haystack()
            all_sprites.add(haystack)
            haystacks.add(haystack)
        for i in range(random.randrange(2, 3)):
            rock = Rock()
            all_sprites.add(rock)
            rocks.add(rock)
        player.HP = 100
    # 取得輸入
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        
    key_box = pygame.key.get_pressed()
    # 遊戲更新
    all_sprites.update() 
    score += 1
    if player.HP == 0:
        game_over = True
    # 火球和草堆 碰撞判斷
    hits = pygame.sprite.groupcollide(haystacks, fires, True, True)
    for i in hits:
        score += 50 
        haystack = Haystack()
        all_sprites.add(haystack)
        haystacks.add(haystack)
        if random.random() > 0.8:
            gadgat = Gadgat(i.rect.center)
            all_sprites.add(gadgat)
            gadgats.add(gadgat)
    # 飛龍和草堆 碰撞判斷
    hits_1 = pygame.sprite.spritecollide(player, haystacks, True)
    for i in hits_1:
        player.HP -= 10
        haystack = Haystack()
        all_sprites.add(haystack)
        haystacks.add(haystack)    
    # 飛龍和石頭 碰撞判斷
    hits_2 = pygame.sprite.spritecollide(player, rocks, True)
    for i in hits_2:
        player.HP -= 10
        rock = Rock() 
        all_sprites.add(rock)
        rocks.add(rock)  
    # 飛龍和道具 碰撞判斷        
    hits_3 = pygame.sprite.spritecollide(player, gadgats, True)
    for i in hits_3:
        if i.type == 'HPO':
            player.HP += 25
            if player.HP > 100:
                player.HP = 100
                score += 50
        elif i.type == 'PWO':
            player.POWER += 50
            if player.POWER > 100:
                player.POWER = 100
                score += 50
    
    # 畫面顯示  
    screen.blit(pygame.transform.scale(BG_img,(800,400)), (0, 0))
    all_sprites.draw(screen)
    draw_Power(screen, player.POWER, 10, 10)
    draw_HP(screen, player.HP, 10, 25)
    draw_Text(screen, str(score), 18, 50, 50)
    pygame.display.update()

pygame.quit