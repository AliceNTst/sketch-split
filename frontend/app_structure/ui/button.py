import ttkbootstrap as ttk
from ttkbootstrap.constants import *



class StylisedButton():
    def __init__(self, master, width, height, r, text, command, font_size = 10):
        #TODO move colors to store separately
        self.canvas = ttk.Canvas(master, width=width, height=height)
        self.canvas.configure(bg="#624996")
        self.default_color = "#e5ddef"
        self.hover_color = "#9c96d7"
        self.text_color = "#624996"
        self.shape = self.create_shape(self.canvas, 0, 0, width, height, r=r, fill=self.default_color)
        self.label = self.canvas.create_text((width)//2, (height)//2, text=text, fill=self.text_color, font=("Segoe UI", font_size))

        #Click
        self.canvas.tag_bind(self.shape, "<Button-1>", lambda e: command())
        self.canvas.tag_bind(self.label, "<Button-1>", lambda e: command())

        # HOVER
        self.canvas.tag_bind(self.shape, "<Enter>", self.on_enter)
        self.canvas.tag_bind(self.label, "<Enter>", self.on_enter)

        self.canvas.tag_bind(self.shape, "<Leave>", self.on_leave)
        self.canvas.tag_bind(self.label, "<Leave>", self.on_leave)

    def on_enter(self, event):
        self.canvas.itemconfig(self.shape, fill=self.hover_color)

    def on_leave(self, event):
        self.canvas.itemconfig(self.shape, fill=self.default_color)

    def create_shape(self, canvas: ttk.Canvas, x1, y1, x2, y2, r=20, **kwargs):
        points = [
            0, 0,
            y2, y2
        ]
        return canvas.create_arc(points, extent = 180, offset="n", **kwargs)
    
    def pack(self, side, padx = 0, **kwargs):
        self.canvas.pack(side=side, padx = padx, **kwargs)




class SideButtonL(StylisedButton):

    def __init__(self, master, width, height, r, text, command, font_size = 10):
        super().__init__(master=master, width=width, height=height, r=r, text=text, command=command, font_size = font_size)
        
    def create_shape(self, canvas: ttk.Canvas, x1, y1, x2, y2, r=20, **kwargs):
        points = [
            x1+0, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+0, y2,
            x1, y2,
            x1, y2-0,
            x1, y1+0,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    
class SideButtonR(StylisedButton):

    def __init__(self, master, width, height, r, text, command, font_size = 10):
        super().__init__(master=master, width=width, height=height, r=r, text=text, command=command, font_size = font_size)
        
    def create_shape(self, canvas: ttk.Canvas, x1, y1, x2, y2, r=20, **kwargs):
        points = [
            x1+r, y1,
            x2-0, y1,
            x2, y1,
            x2, y1+0,
            x2, y2-0,
            x2, y2,
            x2-0, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    

class PrimaryButton(StylisedButton):

    def __init__(self, master, width, height, r, text, command, font_size = 10):
        super().__init__(master=master, width=width, height=height, r=r, text=text, command=command, font_size = font_size)
        
    def create_shape(self, canvas, x1, y1, x2, y2, r=20, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    

class SecondaryButton(StylisedButton):

    def __init__(self, master, width, height, r, text, command, font_size = 10):
        super().__init__(master=master, width=width, height=height, r=r, text=text, command=command, font_size = font_size)
        self.default_color = "#6c5ce7"
        self.hover_color = "#cecaf0"
        self.canvas.itemconfig(self.shape, fill=self.default_color)

        
    def create_shape(self, canvas, x1, y1, x2, y2, r=20, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)
    



# canvas = ttk.Canvas(tool_bar_right, width=600, height=150)
# button = CanvasButton(canvas, 0, 0, 600, 150, "text", on_click)

# canvas.pack(side="left")

# sbutton = StylisedButton(tool_bar_right, width=600, height=150, r=140, text="text", command = lambda: print("Hi!"))
# sbutton.pack("left")

#super().__init__(master, width=width, height=height)