import ttkbootstrap as ttk



class StylesManager:
    def __init__(self, style):
        self.theme = style
        self.load_themes()
        self.apply_theme(style)



    # def apply_theme(self, theme_name):
    #     self.theme = ColorPalettes[theme_name]
    #     self.current_theme = theme_name

    def load_themes(self):
        self.style = ttk.Style()
        self.style.load_user_themes("styles.json")

    def apply_theme(self, name):
        self.style.theme_use(name)


        


