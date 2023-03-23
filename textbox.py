import pygame as pg
from settings import *

pg.init()
# screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('darksalmon')
COLOR_ACTIVE = pg.Color('darkorange1')
FONT1 = pg.font.Font(UI_FONT, 40)
FONT2 = pg.font.Font(UI_FONT, UI_FONT_SIZE)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT2.render(text, True, self.color)
        self.active = False
        self.return_text = ''


    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.return_text = self.text
                    # self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key != pg.K_SPACE:
                    self.text += event.unicode
                # Re-render the text.
                if self.text:
                    self.txt_surface = FONT1.render(self.text + '.00', True, self.color)
                else:
                    self.txt_surface = FONT2.render('INSERT WAGER', True, pg.Color('darksalmon'))

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, (0,0,0), self.rect, 2)
        


# def main():
#     clock = pg.time.Clock()
#     input_box1 = InputBox(100, 100, 140, 32)
#     input_box2 = InputBox(100, 300, 140, 32)
#     input_boxes = [input_box1, input_box2]
#     done = False

#     while not done:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 done = True
#             for box in input_boxes:
#                 box.handle_event(event)

#         for box in input_boxes:
#             box.update()

#         screen.fill((30, 30, 30))
#         for box in input_boxes:
#             box.draw(screen)

#         pg.display.flip()
#         clock.tick(30)


# if __name__ == '__main__':
#     main()
#     pg.quit()