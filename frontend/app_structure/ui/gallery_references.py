import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageDraw
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from app_structure.ui.button import *
from app_structure.ui.sketch_canvas import *
from app_structure.api.api_requests import *


class Gallery:
    def __init__(self, master,  request: RequestData):
        self.master = master
        self.request = request
        self.images_loaded_number = 0
        self.column_width = 500
        self.loaded = False
        self.canvas = tk.Canvas(master)
        self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.canvas.yview, bootstyle="secondary round")

        self.columns_container = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.columns_container, anchor="nw")
        
        self.canvas.configure(yscrollcommand=self.set_scrollbar)


        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="nsew")

        #updated scrollable area on canvas (every time changes occur); self.canvas.bbox("all") - calculates reqion on all content on canvas
        self.columns_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.columns = 3
        self.col_heights = [0] * self.columns

        self.create_columns()
        self.reload_images()

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.scroll))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        self.canvas.bind("<Configure>", self.adjust_columns_width)
        
        


    def round_corners(self, img, radius):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0) + img.size, radius, fill=255)
        img.putalpha(mask)
        return img

    def fit_column(self, image):
        new_width = self.column_width
        new_height = image.height * (new_width/image.width)
        # new_height = self.column_width
        image.thumbnail((new_width, new_height))
    

    def create_columns(self):
        self.col_heights = [0] * self.columns
        self.frame_columns = []
        for column in range(self.columns):
            self.frame_columns.append(ttk.Frame(self.columns_container))
            self.frame_columns[column].grid(row=0, column=column, sticky="n")

    def load_images(self, images_paths):
        if not images_paths:
            return

        print(f"Loading {len(images_paths)} images: {images_paths}")
        self.loaded = False
    
        for path in images_paths:
    
            img = Image.open(path)
            self.fit_column(img)

            img = self.round_corners(img, 20)

            tk_img = ImageTk.PhotoImage(img)

            #checking wich line has least amount of images (least height)
            col = self.col_heights.index(min(self.col_heights))

            label = ttk.Label(self.frame_columns[col], image=tk_img)
            label.image = tk_img
            label.pack(padx=10, pady=10)
            
            self.col_heights[col] += img.height

        # waits for images to be loaded fully
        self.canvas.update_idletasks()
        self.loaded = True


    def reload_images(self):
        # images_to_reload = self.reference_images.get_loaded_images()
        images_to_reload = self.request.reload()
        self.loaded = False
        for column in self.frame_columns:
            column.destroy()
            self.canvas.update_idletasks()
        self.create_columns()

        self.load_images(images_to_reload)
        



    def scroll(self, event):
        #event.delta returns 120 or -120 with each scroll
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        

    def set_scrollbar(self, first, last):
        self.scrollbar.set(first, last)   
        self.on_scroll()  


    def on_scroll(self, *e):
        if self.loaded == False:
            return
        if self.canvas.yview()[1] >= 0.9:
            next_batch = self.request.next(20)
            self.load_images(next_batch)


    def adjust_columns_width(self, e):
        # 3 columns + breathing space on the right (0.5)
        self.column_width = e.width / 3.5
        self.reload_images()

