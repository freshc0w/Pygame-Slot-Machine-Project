from settings import *
from machine import *
from textbox import InputBox
import pygame
import sys
import json

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('SLOT MACHINE')
        self.clock = pygame.time.Clock() 
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        
        # Set up machine class
        self.machine = Machine()
        self.delta_time = 0 
        
        # Sound 
        main_sound = pygame.mixer.Sound('audio/audio_track.mp3')
        main_sound.play(loops = -1)
        
    def load_game(self):
        try: 
            with open('balance.txt') as balance_value:
                self.machine.currPlayer.balance = int(json.load(balance_value))
        except:
            pass        
        try:
            with open('total_wager.txt') as wagered_value:
                self.machine.currPlayer.total_wager = int(json.load(wagered_value))
        except:
            pass
        try:
            with open('total_wins.txt') as wins_count:
                self.machine.currPlayer.total_won = int(json.load(wins_count))
        except:
            pass
    
    def save_game(self):
        with open('balance.txt', 'w') as balance_value:
            json.dump(self.machine.currPlayer.balance, balance_value)
        
        with open('total_wager.txt', 'w') as wagered_value:
            json.dump(self.machine.currPlayer.total_won, wagered_value)
            
        with open('total_wins.txt', 'w') as wins_count:
            json.dump(self.machine.currPlayer.total_won, wins_count)
    
    def run(self):
        self.load_game()
        
        self.start_time = pygame.time.get_ticks()
        
        input_box = InputBox(1035, 617, 50, 45)
        while True: # Need this to keep window running  
            prev_text = input_box.return_text
            # Handling quit operation
            for event in pygame.event.get():
                self.save_game()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                input_box.handle_event(event)
                    
            if input_box.return_text:
                try:
                    wager = int(input_box.return_text)
                    self.machine.currPlayer.set_bet_size(wager)
                    prev_text = input_box.return_text
                except:
                    input_box.text = prev_text
          
            # Setting up time variables
            self.delta_time = (pygame.time.get_ticks() - self.start_time)/1000
            self.start_time = pygame.time.get_ticks()
            
            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.machine.update(self.delta_time)
            self.screen.blit(self.grid_image, (0, 0))
            input_box.update()
            input_box.draw(self.machine.ui.display_surface)
                
            self.clock.tick(FPS)
        
        

if __name__ == '__main__':
    game = Game()
    game.run()
                
        
        
        