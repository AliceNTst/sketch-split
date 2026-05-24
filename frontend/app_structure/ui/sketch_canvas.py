import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageFilter
import json
import config
from ttkbootstrap.constants import *
from app_structure.ui.button import *
from app_structure.ui.sketch_canvas import *
from app_structure.api.api_requests import *

#if adjusted also change in .get_landdmarks(); if changed ------- also adjust .on_click()
POINT_NAMES = [
    "----------",
    "shoulder-left",
    "shoulder-right",
    "hip-left",
    "hip-right",
    "elbow-left",
    "elbow-right",
    "knee-left",
    "knee-right",
    "wrist-left",
    "wrist-right",
    "ankle-left",
    "ankle-right"
]

POINT_RELATIONS = {
    "shoulder-left" : ["shoulder-right", "hip-left", "elbow-left"],
    "shoulder-right" : ["shoulder-left", "hip-right", "elbow-right"],
    "hip-left" : ["hip-right", "shoulder-left", "knee-left"],
    "hip-right" : ["hip-left" , "shoulder-right", "knee-right"],
    "elbow-left" : ["shoulder-left", "wrist-left"],
    "elbow-right" : ["shoulder-right" , "wrist-right"],
    "knee-left" : ["hip-left", "ankle-left"],
    "knee-right" : ["hip-right" , "ankle-right"],
    "wrist-left" : ["elbow-left"],
    "wrist-right" : ["elbow-right"],
    "ankle-left" : ["knee-left"],
    "ankle-right" : ["knee-right" ]
}

class SketchCanvas:
    def __init__(self, master, styles_manager):
        self.image_path = None
        self.styles_manager = styles_manager
        self.master = master
        self.blurred = False
        #color index for styles_manager color list from get_points_color
        self.point_color_index = 0
        self.text_color_index = 0

        # points holds points info with point name as a key and coords as values
        self.points = {}   # {name: {"x":..., "y":...}}
        self.points_info_lines = {}  #{point_name : [lines_ids]}
        self.lines = {} #{line_id: [points]}

        self.image = None
        self.tk_image = None
        self.scale = 1.0   # useful if you later resize displayed image

        # holds currently chosen point (in combobox)
        self.point_var = tk.StringVar(value=POINT_NAMES[0])

        self.canvas = tk.Canvas(master, cursor="cross")
        self.canvas.configure(bg = self.styles_manager.get_light())
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_click)


    def update_colors(self):
        self.canvas.configure(bg = self.styles_manager.get_light())

    def grid(self, row, column, sticky):
        self.canvas.grid(row=row, column=column, sticky=sticky)
        # self.canvas.bind("<Button-1>", self.on_click)

    def pack(self, fill, expand):
        self.canvas.pack(fill = fill, expand = expand)

    def add_to_paned(self, paned, weight=1):
        paned.add(self.canvas, weight=weight)
        

    # def bind(self, sequence, function):
    #     self.canvas.bind("<Button-1>", self.on_click)

    def toggle_blur(self):
        if not self.blurred:
            blurred_image = self.resized_image.filter(ImageFilter.GaussianBlur(radius=10))
            self.tk_image= ImageTk.PhotoImage(blurred_image)
            self.canvas.itemconfig(self.image_id, image=self.tk_image)
            self.blurred = True
        else:
            self.tk_image= ImageTk.PhotoImage(self.resized_image)
            self.canvas.itemconfig(self.image_id, image=self.tk_image)
            self.blurred = False

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if not path:
            return

        self.image_path = path

        self.image = Image.open(path)
        self.canvas.update_idletasks()
        print(self.canvas.winfo_width())
        print(self.canvas.winfo_height())
        self.resized_image = self.resize_image(self.image, canvas_w=self.canvas.winfo_width(), canvas_h=self.canvas.winfo_height())
        self.tk_image = ImageTk.PhotoImage(self.resized_image)

        self.canvas.delete("all")
        #self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
        # self.canvas.config(width=1920, height=900)
        # self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image, tags="bg")
        self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image, tags="bg")

        # redraw saved points if any
        for name, p in self.points.items():
            self.draw_point(name, p["x"]* self.image_scale, p["y"]* self.image_scale)

    def resize_image(self, image, canvas_w, canvas_h):

        if not self.image:
            return None
        
        image_w, image_h = image.size

        # Compute scale factor (keep aspect ratio)
        self.image_scale = min(canvas_w / image_w, canvas_h / image_h)

        new_w = int(image_w * self.image_scale)
        new_h = int(image_h * self.image_scale)

        # Resize image
        resized = image.resize((new_w, new_h), Image.LANCZOS)

        return resized

    def on_resize(self, *args):
        if not self.image:
            return 
        
        print('Message start')
        print(*args)
        print('Message end')
        self.resized_image = self.resize_image(self.image, canvas_w=self.canvas.winfo_width(), canvas_h=self.canvas.winfo_height())
        image = self.resized_image
        if self.blurred == True:
            image = self.resized_image.filter(ImageFilter.GaussianBlur(radius=10))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(self.image_id, image=self.tk_image)
        for name, p in self.points.items():
            self.canvas.delete(f"point_{name}")
            self.draw_point(name, p["x"]* self.image_scale, p["y"]* self.image_scale)
            print(f'{p["x"]}, {p["y"]}')

        # for point in list(self.points_info_lines.keys()):
        #     self.remove_lines_for(point)
        #     self.add_lines_for(point)
        self.update_lines()

    def on_click(self, event):
        if self.tk_image is None:
            return

        point_name = self.point_var.get()

        if point_name == "----------":
            return

        x = event.x
        y = event.y

        original_x = x/self.image_scale
        original_y = y/self.image_scale
        #Save points relative to original image size
        self.points[point_name] = {"x": original_x, "y": original_y}

        # remove old drawing for this point and redraw
        self.canvas.delete(f"point_{point_name}")
        self.draw_point(point_name, x, y)

        self.remove_lines_for(point_name)
        self.add_lines_for(point_name)
        


    def add_lines_for(self, point_name):
        for end_point in POINT_RELATIONS[point_name]:
            if end_point in self.points:
                line_id = self.draw_line(self.points[point_name]["x"]*self.image_scale, self.points[point_name]["y"]*self.image_scale, self.points[end_point]["x"]*self.image_scale, self.points[end_point]["y"]*self.image_scale)
                print(f"Draw line: {point_name} - {end_point}: {line_id}")
                if not end_point in self.points_info_lines:
                    self.points_info_lines[end_point] = []
                self.points_info_lines[end_point].append(line_id)
                self.lines[line_id] = [point_name, end_point]

                if not point_name in self.points_info_lines:
                    self.points_info_lines[point_name] = []
                self.points_info_lines[point_name].append(line_id)


        print(f"Lines added for point: {point_name}")
        print(f"Current lines info: {self.lines}")

    def remove_lines_for(self, point_name):
        if not point_name in self.points_info_lines:
            return
        
        if len(self.points_info_lines[point_name]) == 0:
            return

        for line in list(self.points_info_lines[point_name]):
            for end_point in POINT_RELATIONS[point_name]:
                if end_point in self.points_info_lines:
                    if line in self.points_info_lines[end_point]:
                        self.points_info_lines[end_point].remove(line)
                        print(f"Remove line: {point_name} - {end_point} : {line}")
                        self.canvas.delete(line)
                        self.lines.pop(line)

        self.points_info_lines[point_name] = []
        print(f"Lines removed from point: {point_name}")
        print(f"Current lines info: {self.lines}")

    def update_lines(self):
       
        print("Update lines: ")
        for line in list(self.lines.keys()):
            start_point = self.lines[line][0]
            end_point = self.lines[line][1]
            self.canvas.delete(line)
            new_line = self.draw_line(self.points[start_point]["x"]*self.image_scale, self.points[start_point]["y"]*self.image_scale, self.points[end_point]["x"]*self.image_scale, self.points[end_point]["y"]*self.image_scale)
            print(f"Remove line: {start_point} - {end_point} : {line}")
            self.lines.pop(line)
            print(f"Add line: {start_point} - {end_point} : {new_line}")
            self.lines[new_line] = [start_point, end_point]
            print("Adjust points info lines: change old line index to new one")
            print(f"Points info lines before: {self.points_info_lines}")
            for point in list(self.points_info_lines.keys()):
                self.points_info_lines[point] = [new_line if line_id == line else line_id for line_id in list(self.points_info_lines[point])]
            print(f"Points info lines adjusted: {self.points_info_lines}")

        print(f"Lines updated")
        print(f"Current lines info: {self.lines}")
    
    def _get_color(self, index):
        return self.styles_manager.get_points_color()[index]

    def draw_point(self, name, x, y):
        r = 6
        self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=self._get_color(self.point_color_index), outline="black",
            tags=(f"point_{name}",)
        )
        self.canvas.create_text(
            x + r + 8, y + r - 8,
            text=name,
            anchor="nw",
            fill=self._get_color(self.text_color_index),
            tags=(f"point_{name}",)
        )

    def draw_line(self, x1, y1, x2, y2):
        line = self.canvas.create_line(
        x1, y1,
        x2, y2,
        width=2,
        fill=self.styles_manager.get_light())
        return line

    def set_point_color_index(self, index):
        self.point_color_index = index

    def set_text_color_index(self, index):
        self.text_color_index = index

    def clear_selected(self):
        name = self.point_var.get()
        self.points.pop(name, None)
        self.canvas.delete(f"point_{name}")
        # self.info.config(text=f"Cleared {name}")

        self.remove_lines_for(name)

    def clear_all(self):
        print("Remove all points")
        # for name, p in self.points.items():
        for name in POINT_NAMES[1:]:
            self.points.pop(name, None)
            self.canvas.delete(f"point_{name}")
            print(f"Removed {name}")
        print(f"Current points data: {self.points}")

        print("Remove all lines")
        for line in list(self.lines.keys()):
            self.canvas.delete(line)
            self.lines.pop(line)
            print(f"Removed line: {line}")
        print(f"Current lines: {self.lines}")
        self.points_info_lines.clear()
        print(f"Current point info lines: {self.points_info_lines}")
        

    def export_json(self):
        if not self.points:
            messagebox.showinfo("No points", "No points to export.")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.points, f, indent=2)

        messagebox.showinfo("Saved", f"Saved to {path}")


    def get_landmarks(self):
        if not self.points:
            return None
        
        get_point = lambda _name: [self.points[_name]["x"], self.points[_name]["y"]]
        landmarks = [config.no_point_value]*33
        for point_name in self.points.keys():
            # if point_name == "shoulder-left":
            #     landmarks[11] = get_point(point_name)
            match point_name:
                case "shoulder-left":
                    landmarks[11] = get_point(point_name)
                case "shoulder-right":
                    landmarks[12] = get_point(point_name)
                case "hip-left":
                    landmarks[23] = get_point(point_name)
                case "hip-right":
                    landmarks[24] = get_point(point_name)
                case "elbow-right":
                    landmarks[14] = get_point(point_name)
                case "elbow-left":
                    landmarks[13] = get_point(point_name)
                case "knee-right":
                    landmarks[26] = get_point(point_name)
                case "knee-left":
                    landmarks[25] = get_point(point_name)
                case "wrist-right":
                    landmarks[16] = get_point(point_name)
                case "wrist-left":
                    landmarks[15] = get_point(point_name)
                case "ankle-right":
                    landmarks[28] = get_point(point_name)
                case "ankle-left":
                    landmarks[27] = get_point(point_name)
                case _:
                    print(f"ATTENTION - strange naming for point in sketch: {point_name}")

        # landmarks = numpy.array(landmarks)
        return landmarks



