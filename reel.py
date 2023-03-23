from settings import *
import pygame, random

class Reel:
    def __init__(self, pos):
        
        # Create a container that can store all 5 symbol in a single reel.
        self.symbol_list = pygame.sprite.Group()
        
        # Randomly shuffle the symbols to be placed onto the reel.
        self.shuffled_keys = list(SYMBOLS.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5] # Restrict to have 5 symbols in a single reel at the same time.
        
        self.reel_is_spinning = False 
        
        # Sounds 
        # self.stop_sound = pygame.mixer.Sound()
        # self.stop_sound.set_volume(0.5)
        
        # Using the shuffled keys, add symbols correspondingly to each reel.
        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(SYMBOLS[item], pos, idx,))
            pos = list(pos)
            pos[1] += DEFAULT_IMAGE_SIZE[1] # Moves down by a single square periodically.
            pos = tuple(pos)
            
    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False 
            
            # Stop reel when spin time runs out.
            if self.spin_time < 0:
                reel_is_stopping = True 
            
            if self.delay_time <= 0:
                
                # iterate through all 5 symbols in reel; truncate; add new random symbol on top of stack.
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 50 # every tick, each symbols in reels will move downwards by 50 pixels.
                    
                    # Correct spacing is dependent on the above addition eventually hitting 800ms.
                    if symbol.rect.top == 800:
                        if reel_is_stopping:
                            self.reel_is_spinning = False 
                            # self.stop_sound.play()
                        
                        symbol_idx = symbol.idx 
                        symbol.kill()
                        
                        # spawn rnadom symbol after removing a symbol
                        self.symbol_list.add(Symbol(SYMBOLS[random.choice(self.shuffled_keys)],
                                                    (symbol.x_val, -DEFAULT_IMAGE_SIZE[1]), symbol_idx))
                    
                
    
    def start_spin(self, delay_time):
        self.delay_time = delay_time 
        self.spin_time = 1000 + delay_time 
        self.reel_is_spinning = True 
        
    def reel_spin_result(self):
        # Get and return text representation of symbols in a given reel.
        spin_symbols = []
        for i in GAME_INDICES:
            spin_symbols.append(self.symbol_list.sprites()[i].sym_name)
        return spin_symbols[::-1]
            
class Symbol(pygame.sprite.Sprite):
    def __init__(self, path_to_file, pos, idx):
        super().__init__()
        
        # Symbol type in a friendly name
        self.sym_name = path_to_file.split('/')[3].split('.')[0]
        
        self.pos = pos 
        self.idx = idx 
        self.image = pygame.image.load(path_to_file).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.x_val = self.rect.left # Keeping track of the x value of each rectangle.
        
        # Used for win animations
        self.size_x = DEFAULT_IMAGE_SIZE[0]
        self.size_y = DEFAULT_IMAGE_SIZE[1]
        self.alpha = 255
        self.fade_out = False 
        self.fade_in = False
        
    def update(self):
        # Moves symbols slightly.
        if self.fade_in:
            if self.size_x < 230:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, 
                                                    (self.size_x, self.size_y))
                
        # Fades out non-winning symbols 
        elif not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7 # Decreases image res?
                self.image.set_alpha(self.alpha) 
        