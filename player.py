from settings import *

class Player:
    def __init__(self):
        self.balance = 1000.00
        self.bet_size = 10.00
        self.last_payout = 0.00
        self.total_won = 0.00
        self.total_wager = 0.00
        
        self.data = {}
        self.data['balance'] = self.balance 
        self.data['bet_size'] = self.bet_size 
        self.data['last_payout'] = self.last_payout
        self.data['total_won'] = self.total_won 
        self.data['total_wager'] = self.total_wager
        
        
    def get_data(self):
        player_data = {}
        player_data['balance'] = "{:.2f}".format(self.balance)
        player_data['bet_size'] = "{:.2f}".format(self.bet_size)
        player_data['last_payout'] = "{:.2f}".format(self.last_payout) if self.last_payout else "N/A"
        player_data['total_won'] = "{:.2f}".format(self.total_won)
        player_data['total_wager'] = "{:.2f}".format(self.total_wager)
        
        return player_data

    def set_bet_size(self, value):
        self.bet_size = value

    def place_bet(self):
        bet = self.bet_size
        self.balance -= bet 
        self.total_wager += bet
    
