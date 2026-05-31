import ttkbootstrap as ttk
from ttkbootstrap.constants import *



class StylesManager:
    def __init__(self, theme):
        self.current_theme = theme
        self.load_themes()
        self.apply_theme(theme)

        self.themes = self.style.theme_names()[18:]
        self.current_theme_number = self.themes.index(theme)


    def load_themes(self):
        self.style = ttk.Style()
        self.style.load_user_themes("styles.json")

    def apply_theme(self, name):
        self.style.theme_use(name)

    def next_theme(self):
        print(self.style.theme_names())
        print(self.themes)
        if self.current_theme_number == len(self.themes) - 1:
            self.current_theme_number = 0
        else:
            self.current_theme_number += 1

        self.apply_theme(self.themes[self.current_theme_number])

    def get_primary(self):
        return self.style.colors.primary

    def get_secondary(self):
        return self.style.colors.secondary
    
    def get_success(self):
        return self.style.colors.success
    
    def get_active(self):
        return self.style.colors.active
    
    def get_light(self):
        return self.style.colors.light
    
    def get_bg(self):
        return self.style.colors.bg
    
    def get_points_color(self):
        """Colors should relate with get_text_biitstyles"""
        return [self.style.colors.light, self.style.colors.dark, self.style.colors.danger]
    
    def get_text_bootstyles(self):
        """Colors should relate with get_points_color"""
        return [SECONDARY, DARK, DANGER]

        


