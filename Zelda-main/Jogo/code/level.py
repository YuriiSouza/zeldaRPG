import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout

class Level:
    def __init__(self):
        
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        #sprite setup
        self.create_map()
        
        
    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('C:/Users/yurip/OneDrive/Documentos/GitHub/zeldaRPG/Zelda-main/Jogo/map/mapa_floorBlocks.csv')
        }
        
        for styles, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':    
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if styles == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                            
        self.player = Player((1100,1705), [self.visible_sprites],self.obstacle_sprites)
        
        
        
    def run(self):
        #update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        
        
        
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        #creating the floor
        self.floor_surf = pygame.image.load("C:/Users/yurip/OneDrive/Documentos/GitHub/zeldaRPG/Zelda-main/Jogo/graphics/map/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))
    
    def custom_draw(self, player):
        
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        #drawing the floor
        self.floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, self.floor_offset_pos)
        
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset  
            self.display_surface.blit(sprite.image,offset_pos)
            
        