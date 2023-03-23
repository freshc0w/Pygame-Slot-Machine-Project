from settings import *
import pygame, random

class Reel:
    def __init__(self, pos):
        
        # need to initialise a container class to hold multiple sprite objects.
        self.symbol_list = pygame.sprite.Group() 
        
        # Randomly shuffle the symbols so they are spawned randomly.
        self.shuffled_keys = list(SYMBOLS.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5] # Only matters when there are more than 5 SYMBOLS.
        
        self.reel_is_spinning = False 
        
        # Sounds 
        # self.stop_sound = pygame.mixer.Sound('audio/stop.mp3')
        # self.stop_sound.set_volume(0.5)
        
        # Generating random SYMBOLS in the grid VERTICALLY using the symbol class.
        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(SYMBOLS[item], pos, idx)) # Remember, pos is the tuple(x_top_left, y_top_left)
            pos = list(pos)
            pos[1] += DEFAULT_IMAGE_SIZE[1] # moves down by a square.
            pos = tuple(pos)
            
    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False
            
            # Stop reel when spin time runs out.
            if self.spin_time < 0:
                reel_is_stopping = True 
            
            # Stagger reel spin start animation
            if self.delay_time <= 0:
                
                # Iterate through all 5 symbols in reel; truncatel add new random symbol on top of stack.
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 50 # every tick, each symbols in reels will move downwards by 100 pixels.

                    # Correct spacing is dependent on the above addition eventually hitting 1200
                    if symbol.rect.top == 800:
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                            # self.stop_sound.play()
                            
                        symbol_idx = symbol.idx
                        symbol.kill()
                        # Spawn random symbol in place of the above.
                        self.symbol_list.add(Symbol(SYMBOLS[random.choice(self.shuffled_keys)],
                                                    ((symbol.x_val), -DEFAULT_IMAGE_SIZE[1]), symbol_idx))
                        
    def start_spin(self, delay_time):
        self.delay_time = delay_time 
        self.spin_time = 1000 + delay_time 
        self.reel_is_spinning = True

class Symbol(pygame.sprite.Sprite):
    def __init__(self, path_to_file, pos, idx):
        super().__init__()
        
        # Symbol name
        self.sym_type = path_to_file.split('/')[3].split('.')[0]
        
        self.pos = pos
        self.idx = idx
        self.image = pygame.image.load(path_to_file).convert_alpha() # making png bg to be invisible.
        self.rect = self.image.get_rect(topleft = pos)
        self.x_val = self.rect.left # keep track of a x value.
        
    def update(self):
        pass