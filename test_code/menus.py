import gc9a01 as lcd
import italicc
import NotoSansMono_32 as font




class Menu:
    def __init__(self, menu_name, menu_screen, fg=lcd.WHITE, bg=lcd.BLACK, ac=lcd.MAGENTA):
        self.view = menu_screen
        self.name = menu_name
        self.fg = fg
        self.bg = bg
        self.ac = ac
        
    def display(self):
        h = self.view.height()
        l = self.view.width()
        name_len = self.view.write_len(font, self.name)
        self.view.fill(self.bg)
        self.view.write(font, self.name, int((l/2)-(name_len/2)), 10, self.fg, self.ac)
        
        
        