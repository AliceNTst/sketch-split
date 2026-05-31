import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app_structure.ui import main_window
from app_structure.styles_manager import StylesManager



app = ttk.Window(title= 'SPRY', size=[1920, 1080])

styles_manager = StylesManager("violet")

main_window.MainWindow(app, styles_manager)

app.iconbitmap("assets/icon.ico")

app.mainloop()