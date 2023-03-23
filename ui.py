from player import Player
from textbox import InputBox
from settings import *
import pygame, random

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font, self.bet_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE), pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        self.win_text_angle = random.randint(-4, 4)
        self.display_info()

    def display_info(self):
        player_data = self.player.get_data()
        
        # balance, bet size and total won.
        balance_surf = self.font.render("Balance : $" + player_data['balance'], True, TEXT_COLOR, None)
        x1, y1 = 20, self.display_surface.get_size()[1] - 50
        balance_rect = balance_surf.get_rect(bottomleft = (x1, y1))
        
        bet_surf = self.bet_font.render("Total wagered : $" + player_data['total_wager'], True, TEXT_COLOR, None)
        x2, y2 = self.display_surface.get_size()[0] - bet_surf.get_width() - 30, y1 + 45
        bet_rect = bet_surf.get_rect(bottomleft = (x2, y2))
        
        winnings_surf = self.font.render("Total winnings : $" + player_data['total_won'], True, TEXT_COLOR, None)
        # x1, y2 = 20, self.display_surface.get_size()[1] - 60
        winnings_rect = winnings_surf.get_rect(bottomleft = (x1, y2))
        
        set_wager_surf = self.font.render("Set Wager : $" , True, TEXT_COLOR, None)
        set_wager_rect = set_wager_surf.get_rect(bottomleft = (x2, y1))
        
        # Set input box
        # self.input_box = InputBox(x2 + set_wager_surf.get_width() + 10,
        #                      y1 - set_wager_surf.get_height() - 5,
        #                      set_wager_surf.get_width() - 25,
        #                      set_wager_surf.get_height() + 10)
        # self.input_box.update()
        # self.input_box.draw(self.display_surface)
        
        # Draw player data 
        def draw(surf, rect):
            pygame.draw.rect(surf, False, rect)
            self.display_surface.blit(surf, rect)
            
        draw(balance_surf, balance_rect)
        draw(bet_surf, bet_rect)
        draw(winnings_surf, winnings_rect)
        draw(set_wager_surf, set_wager_rect)

        
        # print last win if applicable
        if self.player.last_payout:
            last_payout = player_data['last_payout']
            win_surf = self.win_font.render(" WIN: $" + last_payout, True, TEXT_COLOR, None)
            x1 = 800 
            y1 = self.display_surface.get_size()[1] - 60
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center = (600, y1))
            self.display_surface.blit(win_surf, win_rect) 
                
    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, HEIGHT-100, WIDTH, 100))
        self.display_info()