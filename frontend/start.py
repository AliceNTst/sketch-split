import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app_structure.ui import main_window
from app_structure.styles_manager import StylesManager
import styles



app = ttk.Window(title= 'sketch', size=[1920, 1080])

styles_manager = StylesManager("violet")
# styles_manager.load_themes()

# style = ttk.Style()
# style.register_theme(styles.theme_green)
# style.theme_use("green")

main_window.MainWindow(app, styles_manager)

app.mainloop()