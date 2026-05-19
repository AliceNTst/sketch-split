import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app_structure.ui import main_window
from app_structure.styles_manager import StylesManager
from PIL import Image, ImageTk



app = ttk.Window(title= 'SPRY', size=[1920, 1080])

styles_manager = StylesManager("violet")
# styles_manager.load_themes()

# style = ttk.Style()
# style.register_theme(styles.theme_green)
# style.theme_use("green")

main_window.MainWindow(app, styles_manager)

# icon = ImageTk.PhotoImage(file="assets/icon.jpg")
# app.iconphoto(True, icon)
app.iconbitmap("assets/icon.ico")

app.mainloop()