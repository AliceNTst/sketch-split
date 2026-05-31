import ttkbootstrap as ttk
from ttkbootstrap.constants import *



class StylisedButton():
    def __init__(self, master, width, height, r, text, command, styles_manager = None, font_size = 10, bg_style = "primary"):
        self.bg_style = bg_style
        self.text = text

        self.styles_manager = styles_manager
        self.canvas = ttk.Canvas(master, width=width, height=height)
        
        self.__set_colors()
        self.shapes = self.create_shape(self.canvas, 0, 0, width, height, r=r, fill=self.default_color)
        self.label = self.canvas.create_text((width)/2, (height)/2, text=text, fill=self.text_color, font=("Segoe UI", font_size))

        #Click
        for shape in self.shapes:
            self.canvas.tag_bind(shape, "<Button-1>", lambda e: command())
        self.canvas.tag_bind(self.label, "<Button-1>", lambda e: command())

        # HOVER
        for shape in self.shapes:
            self.canvas.tag_bind(shape, "<Enter>", self.on_enter)
        self.canvas.tag_bind(self.label, "<Enter>", self.on_enter)

        for shape in self.shapes:
            self.canvas.tag_bind(shape, "<Leave>", self.on_leave)
        self.canvas.tag_bind(self.label, "<Leave>", self.on_leave)
        

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
        more_rectangular_shape = canvas.create_polygon(points, smooth=True, **kwargs)
        return [more_rectangular_shape]
    
    def get_text(self):
        return self.text
    
    def change_text_to(self, text):
        print(f"Change label text to {text}")
        self.canvas.itemconfig(self.label, text=text)
        self.text = text

    def on_enter(self, event):
        for shape in self.shapes:
            self.canvas.itemconfig(shape, fill=self.hover_color)

    def on_leave(self, event):
        for shape in self.shapes:
            self.canvas.itemconfig(shape, fill=self.default_color)
    
    def pack(self, side, padx = 0, **kwargs):
        self.canvas.pack(side=side, padx = padx, **kwargs)

    def __set_colors(self):
        if self.styles_manager != None:
            match self.bg_style:
                case "primary":
                    self.canvas.configure(bg = self.styles_manager.get_primary())
                case "secondary":
                    self.canvas.configure(bg = self.styles_manager.get_secondary())
                case "light":
                    self.canvas.configure(bg = self.styles_manager.get_light())
                case "bg":
                    self.canvas.configure(bg = self.styles_manager.get_bg())
            # self.canvas.configure(bg = self.styles_manager.get_primary())
            self.default_color = self.styles_manager.get_success()
            self.hover_color = self.styles_manager.get_active()
            self.text_color = self.styles_manager.get_primary()
        
        else:
            print("Styles manager was not given to button. Please add styles manager while creating Custom Button")
        
        

    def update_colors(self):
        self.__set_colors()
        for shape in self.shapes:
            self.canvas.itemconfig(shape, fill=self.default_color)
        if self.label != None:
            self.canvas.itemconfig(self.label, fill=self.text_color)
        


class SideButtonL(StylisedButton):

    def __init__(self, master, width, height, r, text, command, styles_manager = None, font_size = 10, bg_style = "primary"):
        super().__init__(master=master, width=width, height=height, r=r, text=text, command=command, styles_manager= styles_manager, font_size = font_size, bg_style=bg_style)
        
    def create_shape(self, canvas: ttk.Canvas, x1, y1, x2, y2, r=20, **kwargs):
        height = y2 - y1
        if r is None:
            r = height // 2

        # Ensure radius is not too large
        r = min(r, height // 2, (x2 - x1) // 2)

        # Center rectangle
        rect = canvas.create_rectangle(
            x1, y1,
            x2 - r, y2,
            outline="",
            **kwargs
        )

        # Right circle
        right = canvas.create_oval(
            x2 - 2 * r, y1,
            x2, y2,
            outline="",
            **kwargs
        )
        return [rect, right]
    
class SideButtonR(StylisedButton):

    def __init__(self, master, width, height, r, text, command, styles_manager = None, font_size = 10, bg_style = "primary"):
        super().__init__(master=master, width=width, height=height, r=r, text=text, command=command, styles_manager= styles_manager, font_size = font_size, bg_style = bg_style)
        
    def create_shape(self, canvas: ttk.Canvas, x1, y1, x2, y2, r=20, **kwargs):
        height = y2 - y1
        if r is None:
            r = height // 2

        # Ensure radius is not too large
        r = min(r, height // 2, (x2 - x1) // 2)

        # Center rectangle
        rect = canvas.create_rectangle(
            x1 + r, y1,
            x2, y2,
            outline="",
            **kwargs
        )

        # Left circle
        left = canvas.create_oval(
            x1, y1,
            x1 + 2 * r, y2,
            outline="",
            **kwargs
        )

        return [rect, left]
    

class PrimaryButton(StylisedButton):

    def __init__(self, master, width, height, r, text, command, styles_manager = None, font_size = 10, bg_style = "primary"):
        super().__init__(master=master, width=width, height=height, r=r, text=text, command=command, styles_manager= styles_manager, font_size = font_size, bg_style = bg_style)
        
    def create_shape(self, canvas: ttk.Canvas, x1, y1, x2, y2, r=20, **kwargs):
        height = y2 - y1
        if r is None:
            r = height // 2

        # Ensure radius is not too large
        r = min(r, height // 2, (x2 - x1) // 2)

        # Center rectangle
        rect = canvas.create_rectangle(
            x1 + r, y1,
            x2 - r, y2,
            outline="",
            **kwargs
        )

        # Left circle
        left = canvas.create_oval(
            x1, y1,
            x1 + 2 * r, y2,
            outline="",
            **kwargs
        )

        # Right circle
        right = canvas.create_oval(
            x2 - 2 * r, y1,
            x2, y2,
            outline="",
            **kwargs
        )
        return [rect, left, right]
    

class SecondaryButton(StylisedButton):

    def __init__(self, master, width, height, r, text, command, styles_manager = None, font_size = 10, bg_style="bg"):
        self.text = text
        self.bg_style = bg_style

        self.styles_manager = styles_manager
        self.canvas = ttk.Canvas(master, width=width, height=height)
        
        self.__set_colors()
        self.shapes = self.create_shape(self.canvas, 0, 0, width, height, r=r, fill=self.default_color)
        self.label = self.canvas.create_text((width)/2, (height)/2, text=text, fill=self.text_color, font=("Segoe UI", font_size))

        #Click
        for shape in self.shapes:
            self.canvas.tag_bind(shape, "<Button-1>", lambda e: command())
        self.canvas.tag_bind(self.label, "<Button-1>", lambda e: command())

        # HOVER
        for shape in self.shapes:
            self.canvas.tag_bind(shape, "<Enter>", self.on_enter)
        self.canvas.tag_bind(self.label, "<Enter>", self.on_enter)

        for shape in self.shapes:
            self.canvas.tag_bind(shape, "<Leave>", self.on_leave)
        self.canvas.tag_bind(self.label, "<Leave>", self.on_leave)


    def __set_colors(self):
        if self.styles_manager != None:
            match self.bg_style:
                case "primary":
                    self.canvas.configure(bg = self.styles_manager.get_primary())
                case "secondary":
                    self.canvas.configure(bg = self.styles_manager.get_secondary())
                case "light":
                    self.canvas.configure(bg = self.styles_manager.get_light())
                case "bg":
                    self.canvas.configure(bg = self.styles_manager.get_bg())
            # self.canvas.configure(bg = self.styles_manager.get_bg())
            self.default_color = self.styles_manager.get_primary()
            self.hover_color = self.styles_manager.get_success()
            self.text_color = self.styles_manager.get_light()
        
        else:
            print("Styles manager was not given to button. Please add styles manager while creating Custom Button")

    def update_colors(self):
        self.__set_colors()
        for shape in self.shapes:
            self.canvas.itemconfig(shape, fill=self.default_color)
        if self.label != None:
            self.canvas.itemconfig(self.label, fill=self.text_color)



class SecondarySideButtonL(SecondaryButton):

    def __init__(self, master, width, height, r, text, command, styles_manager = None, font_size = 10):
        super().__init__(master=master, width=width, height=height, r=r, text=text, command=command, styles_manager= styles_manager, font_size = font_size)
        
    def create_shape(self, canvas: ttk.Canvas, x1, y1, x2, y2, r=20, **kwargs):
        height = y2 - y1
        if r is None:
            r = height // 2

        # Ensure radius is not too large
        r = min(r, height // 2, (x2 - x1) // 2)

        # Center rectangle
        rect = canvas.create_rectangle(
            x1, y1,
            x2 - r, y2,
            outline="",
            **kwargs
        )

        # Right circle
        right = canvas.create_oval(
            x2 - 2 * r, y1,
            x2, y2,
            outline="",
            **kwargs
        )
        return [rect, right]
    


class CircleButton(StylisedButton):

    def __init__(self, master, styles_manager, r = 10, text = None, command = None, font_size = 10):
        self.text = text
        self.styles_manager = styles_manager
        self.label = None
        self.canvas = ttk.Canvas(master, width=r, height=r)
        self.__set_colors()
        self.shapes = self.create_shape(self.canvas, r=r, fill=self.default_color, outline=self.default_color)
        if text != None:
            self.label = self.canvas.create_text((r)/2, (r)/2, text=text, fill=self.text_color, font=("Segoe UI", font_size))

        #Click
        for shape in self.shapes:
            self.canvas.tag_bind(shape, "<Button-1>", lambda e: command())
        if text != None:
            self.canvas.tag_bind(self.label, "<Button-1>", lambda e: command())

        # HOVER
        for shape in self.shapes:
            self.canvas.tag_bind(shape, "<Enter>", self.on_enter)
        if text != None:
            self.canvas.tag_bind(self.label, "<Enter>", self.on_enter)

        for shape in self.shapes:
            self.canvas.tag_bind(shape, "<Leave>", self.on_leave)
        if text != None:
            self.canvas.tag_bind(self.label, "<Leave>", self.on_leave)


    def __set_colors(self):
        if self.styles_manager != None:
            self.canvas.configure(bg = self.styles_manager.get_light())
            self.default_color = self.styles_manager.get_success()
            self.hover_color = self.styles_manager.get_active()
            self.text_color = self.styles_manager.get_primary()
        
        else:
            print("Styles manager was not given to button. Please add styles manager while creating Custom Button")

    def update_colors(self):
        self.__set_colors()
        for shape in self.shapes:
            self.canvas.itemconfig(shape, fill=self.default_color, outline=self.default_color)
        if self.label != None:
            self.canvas.itemconfig(self.label, fill=self.text_color)
        

    def create_shape(self, canvas, r=20, **kwargs):
        points = [
            0, 0,
            r, r
        ]
        circle = canvas.create_oval(points, **kwargs)
        return [circle]


