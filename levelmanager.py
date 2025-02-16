import pygame as pg
from os import path
import pickle
from world import World
from player import Player
from enemy import Thorn, Zombie, Dragon
from bonus import HealingPotion,Apple
from ui import BlackScreen, display_text
pg.init()

font_path = 'assets/Fonts/fontfile.ttf'
title_font = pg.font.Font(font_path, 72)
button_font = pg.font.Font(font_path, 36)
title_pos = 200

assets = 'assets/others'
level_path = 'levels/saved_level_data/level_progress'
bg_image = pg.image.load(f'{assets}/BG/BG.png')
class Level:
    def __init__(self, screen, level=1):
        self.level = level
        self.screen = screen
        self.start_time = None
        self.end_time = None
        self.complete = False
        self.enemies = []
        self.bonuses = []
        self.objects = []
        self.level_loaded = False
        self.font = pg.font.SysFont('Comic Sans MS', 20)
        self.level_logo = self.font.render(f'Level {self.level}', True, (0,0,0)) 
        self.load_level()
        
    def load_level(self):
        self.background = pg.transform.scale(bg_image, (self.screen.get_width(), self.screen.get_height()))
        if not self.level_loaded:
            self.level_loaded = True
            self.player = Player(10,50)
            #loading level data
            if path.exists(f'levels/Level{self.level}_data'):
                with open(f'levels/Level{self.level}_data', 'rb') as pickle_in:
                    world_data = pickle.load(pickle_in)
            self.world = World(world_data)
            self.black_screen = BlackScreen(self.screen)
            self.start_time = pg.time.get_ticks()
       
        self.load_objects()
    
    def load_objects(self):
        if self.level == 1:
            self.bonuses.append(Apple(19 * 40, 18 * 40))
            self.bonuses.append(Apple(36 * 40, 15 * 40))
        elif self.level == 2:
            self.bonuses.append(Apple(15 * 40, 12 * 40))
            self.bonuses.append(Apple(19 * 40, 10 * 40))
            self.bonuses.append(HealingPotion(29 * 40, 6 * 40))
            self.objects.append(Thorn(13 * 40, 12 * 40))
            self.objects.append(Thorn(25 * 40, 8 * 40))
        elif self.level == 3:
            self.bonuses.append(Apple(22 * 40, 8 * 40))
            self.bonuses.append(Apple(27 * 40, 8 * 40))
            self.bonuses.append(Apple(33 * 40, 8 * 40))
            self.objects.append(Thorn(11 * 40, 12 * 40))
            self.objects.append(Thorn(17 * 40, 9 * 40))
            self.objects.append(Thorn(24 * 40, 10 * 40))
            self.objects.append(Thorn(25 * 40, 10 * 40))
            self.objects.append(Thorn(30 * 40, 9 * 40))
        elif self.level == 4:
            self.enemies.append(Zombie(20 * 40, 12 * 40, (1 * 40, 27 * 40)))
        elif self.level == 5:            
            self.bonuses.append(HealingPotion(21 * 40, 14 * 40))
            self.enemies.append(Zombie(10 * 40, 15 * 40, (3 * 40, 15 * 40)))
            self.enemies.append(Zombie(30 * 40, 15 * 40, (26 * 40, 32 * 40)))
        elif self.level == 6:
            self.bonuses.append(Apple(14 * 40, 6 * 40))
            self.bonuses.append(Apple(22 * 40, 5 * 40))
            self.objects.append(Thorn(3 * 40, 6 * 40))
            self.objects.append(Thorn(12 * 40, 14 * 40))
            self.objects.append(Thorn(32 * 40, 14 * 40))
        elif self.level == 7:
            self.bonuses.append(Apple(14 * 40, 17 * 40))
            self.bonuses.append(Apple(22 * 40, 17 * 40))
            self.bonuses.append(HealingPotion(10 * 40, 17 * 40))
            self.bonuses.append(HealingPotion(26 * 40, 17 * 40))
            self.objects.append(Thorn(12 * 40, 19 * 40))
            self.objects.append(Thorn(15 * 40, 16 * 40))
            self.objects.append(Thorn(21 * 40, 16 * 40))
            self.objects.append(Thorn(24 * 40, 19 * 40))

            

    def update(self, keys):        
        self.player.update(keys, self.screen.get_width(), self.world.get_tiles())
        # Update bonuses and enemies
        for bonus in self.bonuses:
            bonus.update(self.player)
        for object in self.objects:
            object.update(self.player)
        for enemy in self.enemies:
            enemy.update(self.player)
        
        # Check if all bonuses are used
        self.all_bonuses_used = all(bonus.used for bonus in self.bonuses)
        # Check if all enemiesare dead
        self.all_enemies_dead = all(not enemy.is_alive for enemy in self.enemies)

        # Set complete status: 
        # All bonuses must be used and all enemies must be dead
        if self.all_bonuses_used and self.all_enemies_dead:
            self.end_time = pg.time.get_ticks() if self.end_time == None else self.end_time
            if self.black_screen.animation_played:
                self.complete = True
            
        else:
            self.complete = False

        return self.complete
    
    def draw(self):
        self.screen.blit(bg_image, (0, 0))
        self.world.draw_world(self.screen) 
        for bonus in self.bonuses:
            bonus.draw(self.screen)
        for object in self.objects:
            object.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.player.draw(self.screen)                           
        self.screen.blit(self.level_logo, (20,40))
        if not (self.all_bonuses_used and self.all_enemies_dead):
            self.black_screen.fade(self.start_time, 1)
        else:            
            display_text(self.screen, title_font, "Level Completed", (400, title_pos))
            self.black_screen.fade(self.end_time,-1)