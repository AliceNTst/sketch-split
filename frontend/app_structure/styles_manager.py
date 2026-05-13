import ttkbootstrap as ttk



class StylesManager:
    def __init__(self, theme):
        self.theme = theme
        self.load_themes()
        self.apply_theme(theme)


    # def apply_theme(self, theme_name):
    #     self.theme = ColorPalettes[theme_name]
    #     self.current_theme = theme_name

    def load_themes(self):
        self.style = ttk.Style()
        self.style.load_user_themes("styles.json")

    def apply_theme(self, name):
        self.style.theme_use(name)

    def get_primary(self):
        return self.style.colors.primary

    def get_secondary(self):
        return self.style.colors.secondary
    
    def get_success(self):
        return self.style.colors.success
    
    def get_active(self):
        return self.style.colors.active

        


