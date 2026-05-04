import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import json
# from app_structure.data.image_data import ImageData
import config
import numpy

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

class SketchCanvas:
    def __init__(self, master):
        #TODO color store separately
        self.master = master

        self.points = {}   # {name: {"x":..., "y":..., "z":...}}
        self.image = None
        self.tk_image = None
        self.scale = 1.0   # useful if you later resize displayed image
        self.point_var = tk.StringVar(value=POINT_NAMES[0])

        self.canvas = tk.Canvas(master, cursor="cross")
        self.canvas.configure(bg="#ffffff")
        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_click)




    def grid(self, row, column, sticky):
        self.canvas.grid(row=row, column=column, sticky=sticky)
        # self.canvas.bind("<Button-1>", self.on_click)

    def pack(self, fill, expand):
        self.canvas.pack(fill = fill, expand = expand)

    def add_to_paned(self, paned, weight=1):
        paned.add(self.canvas, weight=weight)
        

    # def bind(self, sequence, function):
    #     self.canvas.bind("<Button-1>", self.on_click)

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if not path:
            return

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
        self.tk_image = ImageTk.PhotoImage(self.resized_image)
        self.canvas.itemconfig(self.image_id, image=self.tk_image)
        for name, p in self.points.items():
            self.canvas.delete(f"point_{name}")
            self.draw_point(name, p["x"]* self.image_scale, p["y"]* self.image_scale)
            print(f'{p["x"]}, {p["y"]}')

    def on_click(self, event):
        if self.tk_image is None:
            return

        point_name = self.point_var.get()

        if point_name == "----------":
            return

        x = event.x
        y = event.y

        original_x = x/self.image_scale
        original_y = y//self.image_scale
        #Save points relative to original image size
        self.points[point_name] = {"x": original_x, "y": original_y}

        # remove old drawing for this point and redraw
        self.canvas.delete(f"point_{point_name}")
        self.draw_point(point_name, x, y)

        # self.info.config(text=f"Saved {point_name}: x={x}, y={y}")

    def draw_point(self, name, x, y):
        r = 5
        self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill="red", outline="black",
            tags=(f"point_{name}",)
        )
        self.canvas.create_text(
            x + 8, y - 8,
            text=name,
            anchor="nw",
            fill="blue",
            tags=(f"point_{name}",)
        )

    def clear_selected(self):
        name = self.point_var.get()
        self.points.pop(name, None)
        self.canvas.delete(f"point_{name}")
        # self.info.config(text=f"Cleared {name}")

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


    # def apply(self):
    #     if not self.points:
    #         return
        
    #     get_point = lambda _name: [self.points[_name]["x"], self.points[_name]["y"]]
    #     landmarks = [config.no_point_value]*33
    #     for point_name in self.points.keys():
    #         # if point_name == "shoulder-left":
    #         #     landmarks[11] = get_point(point_name)
    #         match point_name:
    #             case "shoulder-left":
    #                 landmarks[11] = get_point(point_name)
    #             case "shoulder-right":
    #                 landmarks[12] = get_point(point_name)
    #             case "hip-left":
    #                 landmarks[23] = get_point(point_name)
    #             case "elbow-right":
    #                 landmarks[14] = get_point(point_name)
    #             case "elbow-left":
    #                 landmarks[13] = get_point(point_name)
    #             case "knee-right":
    #                 landmarks[26] = get_point(point_name)
    #             case "knee-left":
    #                 landmarks[25] = get_point(point_name)
    #             case "wrist-right":
    #                 landmarks[16] = get_point(point_name)
    #             case "wrist-left":
    #                 landmarks[15] = get_point(point_name)
    #             case "ankle-right":
    #                 landmarks[28] = get_point(point_name)
    #             case "ankle-left":
    #                 landmarks[27] = get_point(point_name)
    #             case _:
    #                 print("ATTENTION - starnge naming for point in sketch")
        
    #     landmarks = numpy.array(landmarks)
    #     sketch_data = ImageData(landmarks = landmarks)

        # sorted_images = sort_images(sketch= sketch, images=images)
        #  sorted_paths = [image.path for image in sorted_images]
