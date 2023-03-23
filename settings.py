# Display settings 
DEFAULT_IMAGE_SIZE = (220, 200)
FPS = 120
HEIGHT = 700
WIDTH = 1200
START_X, START_Y = 0, -200
X_OFFSET, Y_OFFSET = 20, 0

# Images
BG_IMAGE_PATH = 'graphics/0/bg.png'
GRID_IMAGE_PATH = 'graphics/0/gridline.png'
GAME_INDICES = [1, 2, 3] # 0 and 4 are outside of the play area
SYM_PATH = 'graphics/0/symbols'

# Text 
TEXT_COLOR = 'White'
UI_FONT = 'graphics/kidspace.ttf'
UI_FONT_SIZE = 25
WIN_FONT_SIZE = 70


# 5 symbols for demo
SYMBOLS = {
    'diamond': f"{SYM_PATH}/0_diamond.png",
    'floppy': f"{SYM_PATH}/0_floppy.png",
    'hourglass': f"{SYM_PATH}/0_hourglass.png",
    'seven': f"{SYM_PATH}/0_seven.png",
    'telephone': f"{SYM_PATH}/0_telephone.png"

    # Playing around with different images.
    # 'caleb': f"{SYM_PATH}/caleb.png",
    # 'heath' :f"{SYM_PATH}/heath.png",
}