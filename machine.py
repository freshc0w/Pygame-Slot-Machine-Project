from settings import *
import pygame 
from reel import *
from wins import *
from player import Player
from ui import UI

class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_idx = 0
        self.reels_dict = {} 
        self.can_toggle = True 
        self.spinning = False 
        self.can_animate = False 
        self.win_animation_ongoing = False
        
        # Results
        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        
        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)
        
        # import sounds 
        # self.spin_sound = pygame.mixer.Sound()
        # self.spin_sound.set_volume(0.15)
        # self.win_three = pygame.mixer.Sound()
        # self.win_three - set.volume(0.6)
        # self.win_four = pygame.mixer.Sound()
        # self.win_four.set_volume(0.7)
        # self.win_five = pygame.mixer.Sound()
        # self.win_five.set_volume(0.8)
        
        
    def cooldowns(self):
        # Only lets player spin if all reels are NOT spinning 
        for reel in self.reels_dict:
            if self.reels_dict[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True 
                
        # Check if each reels ARE NOT spinning 
        if not self.can_toggle and [self.reels_dict[reel].reel_is_spinning for reel
                                    in self.reels_dict].count(False) == 5:
            self.can_toggle = True
            self.spin_result = self.get_result()
        
            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                # Play the win sound.
                # self.play_win_sound(self.win_data)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True 
                self.ui.win_text_angle = random.randint(-4, 4)
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        # Checks for space key, ability to toggle spin, and balance to cover bet size
        
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size
            self.currPlayer.last_payout = None
    
            
    def draw_reels(self, delta_time):
        for reel in self.reels_dict:
            self.reels_dict[reel].animate(delta_time)
    
    def spawn_reels(self):
        '''Spawning the reels horizontally (specified row/ by column)
        '''
        
        # If reels_dict is empty, the initial x_top_left and y_top_left
        # coordinates must be established ( VERY TOP LEFT CORNER )
        if not self.reels_dict:
            x_top_left, y_top_left = 10, -DEFAULT_IMAGE_SIZE[1] # 10 to account for the X_OFFSET
        
        while self.reel_idx < 5: # Restrict out of bounds.
            if self.reel_idx > 0:
                
                # Move to the next top left corner.
                x_top_left, y_top_left = x_top_left + (DEFAULT_IMAGE_SIZE[0] + X_OFFSET
                                                       ), y_top_left
                
            self.reels_dict[self.reel_idx] = Reel((x_top_left, y_top_left)) # Need to make reel class.
            self.reel_idx += 1 # Next column
            
    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning 
            self.can_toggle = False
            
            for reel in self.reels_dict:
                self.reels_dict[reel].start_spin(int(reel) * 200) # 200 is the delay in ms.
                # self.spin_sound.play()
                self.win_animation_ongoing = False # cannot win animate if spinning.
                
    def get_result(self):
        for reel in self.reels_dict:
            self.spin_result[reel] = self.reels_dict[reel].reel_spin_result()
        return self.spin_result
    
    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                if row.count(sym) > 2: # potential win
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]
                    
                    # check possible_win for a subsequence longer than 2 and add to hits.
                    if len(longest_seq(possible_win)) > 2: # Has 3 or more matching symbols.
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        
        if hits:
            self.can_animate = True
            return hits
        
    def pay_player(self, win_data, curr_player):
        multiplier = 0
        spin_payout = 0
        
        # Iterate through all matching symbols and pay according to the number of matches.
        for v in win_data.values():
            multiplier += len(v[1]) # index 1 because it is the length of longest_seq(possible_win)
            
        spin_payout = (multiplier * curr_player.bet_size) # multiplier is dictated by num of matches.
        curr_player.balance += spin_payout # add to player's balance.
        self.machine_balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout 
            
    def play_win_sound(self, win_data):
        sum = 0 
        for item in win_data.values():
            sum += len(item[1])
        if sum == 3: self.win_three.play() 
        elif sum == 4: self.win_four.play()
        elif sum == 5: self.win_five.play()  
            
    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                
                # Reverse the row indices
                if k == 1:
                    animation_row = 3
                elif k == 3:
                    animation_row = 1
                else:
                    animation_row = 2
                animation_col = v[1]
                
                for reel in self.reels_dict:
                    if reel in animation_col and self.can_animate: # animate matching > 2 symbols.
                        self.reels_dict[reel].symbol_list.sprites()[animation_row].fade_in = True
                    
                    # Fade out all symbols that is not matched.
                    for symbol in self.reels_dict[reel].symbol_list:
                        if not symbol.fade_in:
                            symbol.fade_out = True
    
    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        
        for reel_idx in self.reels_dict: # Iterating through each Reel() in reels_dict.
            self.reels_dict[reel_idx].symbol_list.draw(self.display_surface)
            self.reels_dict[reel_idx].symbol_list.update()
        
        self.ui.update()
        self.win_animation()